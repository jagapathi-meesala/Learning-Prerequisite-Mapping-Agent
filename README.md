# Learning Prerequisite Mapping Agent

An offline, explainable starter agent that maps prerequisite relationships between topics and creates a learning sequence for a chosen target.

## Features
- Validates a directed topic-prerequisite graph.
- Builds a prerequisite-first learning path.
- Identifies prerequisite topics not yet marked as learned.
- Detects cycles and reports invalid topic references.
- Explains that the sequence is based on supplied relationships, not an authoritative curriculum.

## Quick start
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pytest -q
python3 -m core.cli examples/topic_map.json
```

## Input format
A JSON object with:
- `target_topic`: topic to learn
- `topics`: array of objects with `id`, `name`, and optional `prerequisites` (array of topic IDs)
- `learned_topics`: optional array of topic IDs already learned

## Behavior
- Prerequisites are traversed before the target topic.
- Duplicate IDs, unknown prerequisite references, unknown targets, and cycles are rejected with clear errors.
- A learning path lists only topics that are not already in `learned_topics`.
- Gap analysis returns missing prerequisites for the target and the full prerequisite chain.

## Responsible use
The agent uses only relationships supplied in the input. It does not automatically know the correct prerequisites for every subject, grade, or learner. Teachers and learners should review the map for suitability.

## Limitations
- No LMS integration or automatic assessment of mastery.
- “Learned” status is accepted as supplied; it is not independently tested.
- Suggested ordering cannot replace instructor judgment or adapt to individual performance without additional evidence.
