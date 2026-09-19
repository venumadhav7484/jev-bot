"""Serve the local Jev evidence assistant on loopback only."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from urllib.parse import unquote, urlsplit
from jev_bot import ROOT, answer


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # User ideas and source content do not belong in access logs.

    def trusted(self):
        host = self.headers.get('Host')
        allowed = {f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}'}
        return host in allowed and self.headers.get('Origin') in (None, 'http://'+host)

    def send(self, code, data, content_type='application/json; charset=utf-8'):
        self.send_response(code)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if not self.trusted():
            return self.send(403, b'{"error":"Local access only"}')
        path = unquote(urlsplit(self.path).path)
        static = {'/': ('web/index.html', 'text/html'), '/app.js': ('web/app.js', 'text/javascript'),
                  '/style.css': ('web/style.css', 'text/css')}
        if path in static:
            name, kind = static[path]
            return self.send(200, (ROOT/name).read_bytes(), kind+'; charset=utf-8')
        if path.startswith('/docs/'):
            candidate = (ROOT/path.lstrip('/')).resolve()
            if candidate.is_relative_to(ROOT/'docs') and candidate.suffix in ('.md', '.json') and candidate.is_file():
                return self.send(200, candidate.read_bytes(), 'text/plain; charset=utf-8')
        self.send(404, b'{"error":"Not found"}')

    def do_POST(self):
        if not self.trusted():
            return self.send(403, b'{"error":"Local access only"}')
        if self.path != '/api/answer':
            return self.send(404, b'{"error":"Not found"}')
        if self.headers.get_content_type() != 'application/json':
            return self.send(415, b'{"error":"Expected JSON"}')
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if not 0 < size <= 30000:
                return self.send(413, b'{"error":"Request too large or empty"}')
            self.connection.settimeout(60)
            request = json.loads(self.rfile.read(size))
            if not isinstance(request, dict) or not isinstance(request.get('use_jev', False), bool):
                raise ValueError('Invalid request')
            result = answer(request.get('idea'), request.get('use_jev', False))
            self.send(200, json.dumps(result, ensure_ascii=False).encode())
        except (ValueError, TypeError):
            self.send(400, b'{"error":"Enter an idea of 3 to 6000 characters and a boolean use_jev option."}')
        except Exception:
            self.send(500, b'{"error":"Local evidence could not be loaded. Check the exported snapshot."}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    print(f'Jev-bot: http://127.0.0.1:{server.server_port} — Ctrl+C to stop', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
