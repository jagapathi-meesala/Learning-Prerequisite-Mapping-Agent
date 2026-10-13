from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "agent.yaml", "SOUL.md", "README.md", "RULES.md", "DUTIES.md", "AGENTS.md",
    "EXPLAINABILITY.md", "requirements.txt", ".env.example", ".gitignore", "pytest.ini",
    "core/__init__.py", "core/mapping.py", "core/cli.py",
    "tools/validate-topic-map.yaml", "tools/build-learning-path.yaml",
    "tools/identify-prerequisite-gaps.yaml", "skills/prerequisite-identification/SKILL.md",
    "skills/learning-path-planning/SKILL.md", "skills/gap-analysis/SKILL.md",
    "tests/test_mapping.py", "examples/topic_map.json"
]
missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
if missing:
    print("FAIL: missing required files:")
    print("\n".join(missing))
    sys.exit(1)
print(f"PASS: all {len(REQUIRED)}/{len(REQUIRED)} required files present")
