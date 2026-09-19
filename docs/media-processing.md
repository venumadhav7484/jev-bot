# Local media evidence processing

`process_media.py` turns a local recording into timestamped frame samples, contact sheets and optional speech transcription. `ocr_frames.swift` extracts visible text using macOS Vision. These tools close an acquisition gap: a readable post does not mean its linked video has been inspected.

## Runtime

Use an isolated Python environment with `Pillow` and, for speech, `faster-whisper`. Install `ffmpeg` and `ffprobe` separately. OCR requires macOS, Vision and the Swift compiler. The tested local configuration uses Python 3.12, Whisper base on CPU with int8 computation, and macOS Vision accurate text recognition.

```sh
python scripts/process_media.py /absolute/path/demo.mp4 \
  --source-url https://example.org/original-post --interval 1

swiftc scripts/ocr_frames.swift -o /tmp/jev-ocr-frames
/tmp/jev-ocr-frames /absolute/path/to/extracted/frames > /tmp/jev-ocr.jsonl
```

The first transcription run needs model weights. Add `--allow-model-download` once to permit downloading them; later runs use the local cache. `--skip-transcription` omits speech processing. Media stays on the local machine. These scripts do not call Jev or a paid transcription API and do not load project credentials.

Outputs live in ignored `research/media-analysis/`, keyed by input SHA-256 and extraction configuration. Each manifest records the original source URL, duration, frame interval, transcription model when used, elapsed extraction time, and unresolved review status. Different sampling intervals have separate output directories.

## Review boundary

Extraction does not approve a source or validate an implementation. An editor must inspect the evidence, correct transcription/OCR errors, preserve contradictory claims, and update the private source ledger and case table. A display reading “100%” is not proof of correctness. A video marked “dry run” cannot verify real transaction execution.

Frame sampling can miss brief events. Speech transcription can omit or mishear words; an empty transcript does not prove silence. Inspect audio-track metadata and use denser frames or targeted playback when the claim requires them. Music quality is not evaluated by speech transcription. OCR returns an error record and nonzero exit status if any frame fails.

OCR language handling also matters: the tested default produced badly corrupted Japanese text in one recording. Review the original frames and use an appropriate language configuration before relying on multilingual OCR. Keep this limitation separate from the source application's own behavior.

Keep quoted/reposted media linked to its original source. Deduplicate the media file without merging different authors' claims. Parent posts, reply videos, repositories and inaccessible sources retain separate evidence records.

The frozen capture cursor never advances because media was downloaded, OCR succeeded or a file was backed up. Public exports contain curated summaries; raw captures, local media and credentials remain ignored.
