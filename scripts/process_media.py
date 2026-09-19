"""Extract local media evidence without approving any source claims.

Requires ffmpeg/ffprobe and optional faster-whisper/Pillow in an isolated Python
runtime. All output stays under ignored research/. This tool does not fetch URLs,
load credentials, publish evidence, or modify source-review dispositions.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('--source-url', required=True)
    parser.add_argument('--model', default='base')
    parser.add_argument('--skip-transcription', action='store_true')
    parser.add_argument('--allow-model-download', action='store_true',
                        help='Allow downloading model weights on first use; media stays local')
    parser.add_argument('--interval', type=float, default=1.0)
    args = parser.parse_args()
    if args.interval <= 0:
        parser.error('--interval must be positive')
    source = args.file.resolve(strict=True)
    if not source.is_file():
        parser.error('Input must be a local file')
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    configuration = {'interval_seconds': args.interval, 'model': args.model,
                     'transcribe': not args.skip_transcription, 'version': 1}
    variant = hashlib.sha256(json.dumps(configuration, sort_keys=True).encode()).hexdigest()[:12]
    output = ROOT / 'research/media-analysis' / digest / variant
    output.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    probe = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(source)
    ]))
    (output / 'probe.json').write_text(json.dumps(probe, indent=2) + '\n')
    manifest = {
        'source_url': args.source_url, 'input_file': str(source), 'sha256': digest,
        'extraction_configuration': configuration,
        'duration_seconds': float(probe.get('format', {}).get('duration', 0)),
        'review_status': 'machine_extracted_pending_review',
        'independently_validated': False,
        'limits': ['Sampled frames can miss events between samples.',
                   'Machine transcription may omit or mishear speech.',
                   'Extraction is not editorial review or implementation validation.'],
    }
    if any(s['codec_type'] == 'video' for s in probe['streams']):
        frames = output / 'frames'
        frames.mkdir(exist_ok=True)
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
                        '-vf', f'fps=1/{args.interval}', str(frames / '%05d.jpg')], check=True)
        manifest['frame_interval_seconds'] = args.interval
        manifest['frame_count'] = len(list(frames.glob('*.jpg')))
        from PIL import Image, ImageDraw
        paths = sorted(frames.glob('*.jpg'))
        sheets = []
        for batch in range(0, len(paths), 12):
            subset = paths[batch:batch + 12]
            sheet = Image.new('RGB', (1280, ((len(subset) + 1) // 2) * 430), 'white')
            draw = ImageDraw.Draw(sheet)
            for i, path in enumerate(subset):
                with Image.open(path) as frame:
                    frame.thumbnail((630, 400))
                    x, y = (i % 2) * 640, (i // 2) * 430
                    sheet.paste(frame, (x, y + 25))
                    draw.text((x + 5, y + 5), f'Frame {batch+i+1}; approximately {(batch+i)*args.interval:.1f}s', fill='black')
            target = output / f'contact-{batch//12+1:03d}.jpg'
            sheet.save(target, quality=90)
            sheets.append(str(target))
        manifest['contact_sheets'] = sheets
    if any(s['codec_type'] == 'audio' for s in probe['streams']) and not args.skip_transcription:
        # No media is uploaded. Only the model weights are downloaded on first use.
        os.environ.setdefault('HF_HUB_DISABLE_TELEMETRY', '1')
        from faster_whisper import WhisperModel
        model = WhisperModel(args.model, device='cpu', compute_type='int8',
                             download_root=str(ROOT / 'research/model-cache'),
                             local_files_only=not args.allow_model_download)
        segments, info = model.transcribe(str(source), beam_size=5, vad_filter=True)
        transcript = [{'start': s.start, 'end': s.end, 'text': s.text,
                       'avg_logprob': s.avg_logprob, 'no_speech_prob': s.no_speech_prob}
                      for s in segments]
        (output / 'transcript.json').write_text(json.dumps(transcript, indent=2) + '\n')
        (output / 'transcript.txt').write_text('\n'.join(
            f'[{s["start"]:.2f}-{s["end"]:.2f}] {s["text"]}' for s in transcript) + '\n')
        manifest.update(transcription_model=args.model, language=info.language,
                        language_probability=info.language_probability,
                        transcript_segments=len(transcript))
    manifest['elapsed_seconds'] = round(time.monotonic() - started, 3)
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'output_directory': str(output), **manifest}, indent=2))


if __name__ == '__main__':
    main()
