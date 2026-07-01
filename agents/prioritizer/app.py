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
logger = logging.getLogger("prioritizer")
logger.addHandler(handler)
logger.setLevel(logging.INFO)

INPUT_FILE = "/data/summary.txt"
OUTPUT_FILE = "/data/prioritized.txt"

PRIORITY_KEYWORDS = [
    "urgent", "today", "asap", "important",
    "deadline", "critical", "action required"
]

def score_line(line):
    """Count how many priority keywords appear in a line."""
    lower = line.lower()
    return sum(1 for kw in PRIORITY_KEYWORDS if kw in lower)

def prioritize():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    scored = [(line, score_line(line)) for line in lines]
    scored.sort(key=lambda x: x[1], reverse=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for line, score in scored:
            out.write(f"[{score}] {line}\n")

    logger.info(f"Prioritized {len(scored)} items -> {OUTPUT_FILE}")

if __name__ == "__main__":
    prioritize()