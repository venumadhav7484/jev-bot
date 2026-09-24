"""Serve the local Jev evidence assistant on loopback only."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import threading
import time
import uuid
from urllib.parse import unquote, urlsplit
from jev_bot import ROOT
from research_answer import answer as research_answer
from backup_private import load_env

JOBS = {}
JOB_LOCK = threading.Lock()


def run_job(identifier, idea, mode, source):
    def progress(update):
        with JOB_LOCK:
            JOBS[identifier]['progress'] = update
    try:
        result = research_answer(idea, mode, source, progress)
        with JOB_LOCK:
            JOBS[identifier].update(status='complete', result=result)
    except (ValueError, RuntimeError, OSError):
        with JOB_LOCK:
            JOBS[identifier].update(status='failed', error='Research answer failed. Check configured API access and the selected snapshot; no provider response body is exposed.')
    except Exception:
        with JOB_LOCK:
            JOBS[identifier].update(status='failed', error='Couldn’t complete this answer. Please retry.')


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
        if path == '/api/config':
            import os
            values = {**load_env(ROOT/'.env.local'), **os.environ}
            return self.send(200, json.dumps({'jev_available': bool(values.get('jev_api_key')),
                'writer_available': bool(values.get('glm_key')), 'writer_model': 'glm-5.3',
                's3_available': (ROOT/'research/storage/latest-backup.json').is_file()}).encode())
        if path.startswith('/api/jobs/'):
            with JOB_LOCK:
                job = JOBS.get(path.removeprefix('/api/jobs/'))
                body = json.dumps(job).encode() if job else None
            return self.send(200, body) if body else self.send(404, b'{"error":"Answer job not found or expired."}')
        static = {'/': ('web/index.html', 'text/html'), '/app.js': ('web/app.js', 'text/javascript'),
                  '/style.css': ('web/style.css', 'text/css'),
                  '/file-input.mjs': ('web/file-input.mjs', 'text/javascript'),
                  '/answer-design.mjs': ('web/answer-design.mjs', 'text/javascript'),
                  '/case-examples.mjs': ('web/case-examples.mjs', 'text/javascript'),
                  '/bot-client.mjs': ('web/bot-client.mjs', 'text/javascript'),
                  '/evidence.mjs': ('web/evidence.mjs', 'text/javascript')}
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
        if self.path not in ('/api/answer', '/api/jobs', '/api/feedback'):
            return self.send(404, b'{"error":"Not found"}')
        if self.headers.get_content_type() != 'application/json':
            return self.send(415, b'{"error":"Expected JSON"}')
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if not 0 < size <= 30000:
                return self.send(413, b'{"error":"Request too large or empty"}')
            self.connection.settimeout(60)
            request = json.loads(self.rfile.read(size))
            if self.path == '/api/feedback':
                from cloud_bot import parse_feedback
                try:
                    identifier, field, value = parse_feedback({'body': json.dumps(request)})
                except (ValueError, TypeError, UnicodeError):
                    return self.send(400, b'{"error":"Send thumbs up/down or a comment of 1 to 2,000 characters."}')
                with JOB_LOCK:
                    job = JOBS.get(identifier)
                    if not job or job['status'] != 'complete' or time.time()-job['created'] >= 86400:
                        return self.send(404, b'{"error":"This answer has expired or is not ready for feedback."}')
                    key = 'feedback_'+field
                    if key in job and job[key] != value:
                        return self.send(409, b'{"error":"Feedback already submitted for this answer."}')
                    if key not in job:
                        folder = ROOT/'research/feedback'
                        folder.mkdir(parents=True, exist_ok=True)
                        with (folder/'local.jsonl').open('a') as out:
                            out.write(json.dumps({'event': 'answer_feedback', 'job_id': identifier,
                                'submitted_at': int(time.time()), field: value})+'\n')
                        job[key] = value
                return self.send(200, b'{"saved":true}')
            if not isinstance(request, dict) or not isinstance(request.get('use_jev', False), bool):
                raise ValueError('Invalid request')
            if self.path in ('/api/jobs', '/api/answer'):
                idea, mode, source = request.get('idea'), request.get('mode', 'evidence'), request.get('source', 'local')
                if not isinstance(idea, str) or not 3 <= len(idea.strip()) <= 6000 or mode not in ('evidence', 'written') or source not in ('local', 's3'):
                    raise ValueError('Invalid research request')
                with JOB_LOCK:
                    for identifier in list(JOBS):
                        if JOBS[identifier]['status'] != 'running' and time.time()-JOBS[identifier]['created'] > 1800:
                            del JOBS[identifier]
                    if any(j['status'] == 'running' for j in JOBS.values()):
                        return self.send(409, b'{"error":"A research answer is already running. Wait for it to finish."}')
                    while len(JOBS) >= 16:
                        del JOBS[next(iter(JOBS))]
                    identifier = uuid.uuid4().hex
                    JOBS[identifier] = {'status': 'running', 'created': time.time(), 'progress': {'stage': 'Starting research evaluation'}}
                threading.Thread(target=run_job, args=(identifier, idea, mode, source), daemon=True).start()
                return self.send(202, json.dumps({'id': identifier}).encode())
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
