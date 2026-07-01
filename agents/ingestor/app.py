import os
import logging

import json
import logging

class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "agent": record.name,
            "message": record.getMessage(),
        })

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger("ingestor")
logger.addHandler(handler)
logger.setLevel(logging.INFO)

INPUT_DIR = "/data/input"
OUTPUT_FILE = "/data/ingested.txt"

def ingest():
    content = ""
    files_processed = 0
    for filename in sorted(os.listdir(INPUT_DIR)):
        filepath = os.path.join(INPUT_DIR, filename)
        if os.path.isfile(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content += f"\n--- {filename} ---\n"
                    content += f.read()
                    content += "\n"
                    files_processed += 1
            except Exception as e:
                logger.error(f"Failed to read {filename}: {e}")

    if files_processed == 0:
        logger.warning("No input files found in /data/input/")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write(content)
    logger.info(f"Ingested {files_processed} files -> {OUTPUT_FILE}")

if __name__ == "__main__":
    ingest()