"""Capture frame.html at 30 fps with one headless Chrome over the DevTools protocol (stdlib only), then encode MP4.

Usage: python capture.py [--seconds 14] [--fps 30] [--only 1.8,4.7]   (--only writes preview PNGs)
"""
import argparse
import base64
import json
import os
import shutil
import socket
import struct
import subprocess
import tempfile
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
PORT = 9333
W, H = 1080, 1350


class WebSocket:
    def __init__(self, url):
        rest = url.split('://', 1)[1]
        hostport, path = rest.split('/', 1)
        host, port = hostport.split(':')
        self.sock = socket.create_connection((host, int(port)), timeout=60)
        key = base64.b64encode(os.urandom(16)).decode()
        self.sock.sendall((f'GET /{path} HTTP/1.1\r\nHost: {hostport}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n'
                           f'Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n').encode())
        head = b''
        while b'\r\n\r\n' not in head:
            head += self.sock.recv(1)
        if b' 101 ' not in head.split(b'\r\n')[0]:
            raise RuntimeError(head.decode(errors='replace'))

    def _read(self, n):
        buf = b''
        while len(buf) < n:
            chunk = self.sock.recv(n - len(buf))
            if not chunk:
                raise ConnectionError('socket closed')
            buf += chunk
        return buf

    def send(self, text):
        data = text.encode()
        header = bytearray([0x81])
        if len(data) < 126:
            header.append(0x80 | len(data))
        elif len(data) < 65536:
            header.append(0x80 | 126)
            header += struct.pack('>H', len(data))
        else:
            header.append(0x80 | 127)
            header += struct.pack('>Q', len(data))
        mask = os.urandom(4)
        self.sock.sendall(bytes(header) + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(data)))

    def recv(self):
        message = b''
        while True:
            b1, b2 = self._read(2)
            fin, opcode, length = b1 & 0x80, b1 & 0x0F, b2 & 0x7F
            if length == 126:
                length = struct.unpack('>H', self._read(2))[0]
            elif length == 127:
                length = struct.unpack('>Q', self._read(8))[0]
            payload = self._read(length)
            if opcode == 0x8:
                raise ConnectionError('closed by browser')
            if opcode == 0x9:
                continue
            message += payload
            if fin:
                return message.decode()


class CDP:
    def __init__(self, ws):
        self.ws, self.next_id = ws, 0

    def call(self, method, **params):
        self.next_id += 1
        self.ws.send(json.dumps({'id': self.next_id, 'method': method, 'params': params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get('id') == self.next_id:
                if 'error' in msg:
                    raise RuntimeError(msg['error'])
                return msg.get('result', {})

    def wait_event(self, name, timeout=30):
        end = time.time() + timeout
        while time.time() < end:
            msg = json.loads(self.ws.recv())
            if msg.get('method') == name:
                return msg
        raise TimeoutError(name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seconds', type=float, default=14.0)
    ap.add_argument('--fps', type=int, default=30)
    ap.add_argument('--only', default='')
    ap.add_argument('--page', default='frame.html')
    ap.add_argument('--out', default='bharat_test.mp4')
    ap.add_argument('--audio', default='')
    ap.add_argument('--music-db', type=float, default=-8.0)
    args = ap.parse_args()

    profile = tempfile.mkdtemp(prefix='bharat-chrome-')
    proc = subprocess.Popen([CHROME, '--headless=new', f'--remote-debugging-port={PORT}', f'--user-data-dir={profile}',
                             f'--window-size={W},{H}', '--hide-scrollbars', '--force-device-scale-factor=1',
                             '--disable-gpu', '--no-first-run', '--no-default-browser-check', 'about:blank'],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(100):
            try:
                targets = json.load(urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json/list', timeout=2))
                page = next(t for t in targets if t.get('type') == 'page')
                break
            except Exception:
                time.sleep(0.2)
        else:
            raise RuntimeError('Chrome did not start')
        cdp = CDP(WebSocket(page['webSocketDebuggerUrl']))
        cdp.call('Emulation.setDeviceMetricsOverride', width=W, height=H, deviceScaleFactor=1, mobile=False)
        cdp.call('Page.enable')
        cdp.call('Page.navigate', url=(HERE / args.page).as_uri() + '?t=0')
        cdp.wait_event('Page.loadEventFired')
        cdp.call('Runtime.evaluate', expression='document.fonts.ready.then(() => 1)', awaitPromise=True)

        if args.only:
            times, outdir = [float(x) for x in args.only.split(',')], HERE / 'preview'
        else:
            n = int(args.seconds * args.fps)
            times, outdir = [i / args.fps for i in range(n)], HERE / 'frames'
            shutil.rmtree(outdir, ignore_errors=True)
        outdir.mkdir(exist_ok=True)
        start = time.time()
        for i, t in enumerate(times):
            cdp.call('Runtime.evaluate', expression=f'renderAt({t})')
            shot = cdp.call('Page.captureScreenshot', format='png')
            name = f't_{t}.png' if args.only else f'f_{i:04d}.png'
            (outdir / name).write_bytes(base64.b64decode(shot['data']))
        print(f'{len(times)} frames in {time.time() - start:.1f}s -> {outdir}')
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
        shutil.rmtree(profile, ignore_errors=True)

    if not args.only:
        out = HERE / args.out
        cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(args.fps), '-i', str(HERE / 'frames' / 'f_%04d.png')]
        if args.audio:
            fade = max(0.0, args.seconds - 3)
            cmd += ['-i', str(HERE / args.audio), '-filter_complex',
                    f'[1:a]volume={args.music_db}dB,afade=t=out:st={fade}:d=3[a]', '-map', '0:v', '-map', '[a]',
                    '-c:a', 'aac', '-b:a', '160k', '-shortest']
        cmd += ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'slow', '-movflags', '+faststart', str(out)]
        subprocess.run(cmd, check=True)
        print('video:', out, out.stat().st_size, 'bytes')


if __name__ == '__main__':
    main()
