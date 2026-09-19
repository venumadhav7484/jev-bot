import Foundation
import Vision
import ImageIO

// Local OCR only. Inputs are extracted images, never executable source code.
guard CommandLine.arguments.count == 2 else {
    FileHandle.standardError.write(Data("Usage: ocr_frames IMAGE_DIRECTORY\n".utf8))
    exit(2)
}
let directory = URL(fileURLWithPath: CommandLine.arguments[1])
let files = try FileManager.default.contentsOfDirectory(at: directory, includingPropertiesForKeys: nil).filter { ["jpg", "png"].contains($0.pathExtension) }.sorted { $0.path < $1.path }
var failures = 0
for file in files {
    autoreleasepool {
        var record: [String: Any] = ["frame": file.lastPathComponent]
        do {
            let request = VNRecognizeTextRequest()
            request.recognitionLevel = .accurate
            request.usesLanguageCorrection = false
            try VNImageRequestHandler(url: file).perform([request])
            record["observations"] = (request.results ?? []).compactMap { observation -> [String: Any]? in
                guard let candidate = observation.topCandidates(1).first else { return nil }
                return ["text": candidate.string, "confidence": candidate.confidence,
                        "bbox": [observation.boundingBox.origin.x, observation.boundingBox.origin.y,
                                 observation.boundingBox.size.width, observation.boundingBox.size.height]]
            }
        } catch {
            failures += 1
            record["error"] = String(describing: error)
        }
        if let data = try? JSONSerialization.data(withJSONObject: record, options: [.sortedKeys]), let line = String(data: data, encoding: .utf8) { print(line) }
    }
}
if failures > 0 { exit(1) }
