"""CLI for learning prerequisite mapping."""
import json
import sys
from pathlib import Path
from core.mapping import validate_topic_map, build_learning_path, identify_prerequisite_gaps

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 -m core.cli <topic_map.json>", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        validation = validate_topic_map(data)
        target = data.get("target_topic")
        learned = data.get("learned_topics", [])
        path = build_learning_path(data, target, learned)
        gaps = identify_prerequisite_gaps(data, target, learned)
        print(json.dumps({"validation": {"valid": validation["valid"], "topic_count": validation["topic_count"]},
                          "learning_path": path, "prerequisite_gaps": gaps}, indent=2))
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
