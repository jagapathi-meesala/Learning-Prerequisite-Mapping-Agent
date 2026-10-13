"""Prerequisite graph validation and learning path generation."""
from typing import Any

def validate_topic_map(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("topic map must be a JSON object.")
    topics = data.get("topics")
    if not isinstance(topics, list) or not topics:
        raise ValueError("topics must be a non-empty list.")
    by_id = {}
    for topic in topics:
        if not isinstance(topic, dict):
            raise ValueError("each topic must be an object.")
        tid, name = topic.get("id"), topic.get("name")
        prereqs = topic.get("prerequisites", [])
        if not isinstance(tid, str) or not tid.strip():
            raise ValueError("topic id must be a non-empty string.")
        if tid in by_id:
            raise ValueError(f"duplicate topic id: {tid}")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"topic {tid}: name must be a non-empty string.")
        if not isinstance(prereqs, list) or any(not isinstance(p, str) for p in prereqs):
            raise ValueError(f"topic {tid}: prerequisites must be a list of topic IDs.")
        if len(set(prereqs)) != len(prereqs):
            raise ValueError(f"topic {tid}: duplicate prerequisite.")
        by_id[tid] = {"id": tid, "name": name, "prerequisites": list(prereqs)}
    for tid, topic in by_id.items():
        for prereq in topic["prerequisites"]:
            if prereq not in by_id:
                raise ValueError(f"topic {tid} references unknown prerequisite: {prereq}")
    visiting, visited = set(), set()
    def visit(tid):
        if tid in visiting:
            raise ValueError(f"cycle detected at topic: {tid}")
        if tid in visited:
            return
        visiting.add(tid)
        for prereq in by_id[tid]["prerequisites"]:
            visit(prereq)
        visiting.remove(tid)
        visited.add(tid)
    for tid in by_id:
        visit(tid)
    return {"topics_by_id": by_id, "topic_count": len(by_id), "valid": True}

def build_learning_path(data: dict[str, Any], target_topic: str, learned_topics: list[str] | None = None) -> dict[str, Any]:
    validated = validate_topic_map(data)
    by_id = validated["topics_by_id"]
    if target_topic not in by_id:
        raise ValueError(f"unknown target topic: {target_topic}")
    learned = learned_topics or data.get("learned_topics", [])
    if not isinstance(learned, list) or any(not isinstance(t, str) for t in learned):
        raise ValueError("learned_topics must be a list of topic IDs.")
    unknown_learned = [t for t in learned if t not in by_id]
    if unknown_learned:
        raise ValueError("unknown learned topic IDs: " + ", ".join(unknown_learned))
    ordered, visited = [], set()
    def visit(tid):
        if tid in visited:
            return
        visited.add(tid)
        for prereq in by_id[tid]["prerequisites"]:
            visit(prereq)
        ordered.append(tid)
    visit(target_topic)
    remaining = [tid for tid in ordered if tid not in set(learned)]
    return {
        "target_topic": by_id[target_topic],
        "full_prerequisite_order": [{"id": tid, "name": by_id[tid]["name"]} for tid in ordered],
        "recommended_learning_path": [{"id": tid, "name": by_id[tid]["name"]} for tid in remaining],
        "already_learned": list(learned),
        "human_review_required": True
    }

def identify_prerequisite_gaps(data: dict[str, Any], target_topic: str, learned_topics: list[str] | None = None) -> dict[str, Any]:
    path = build_learning_path(data, target_topic, learned_topics)
    target_id = target_topic
    missing = [topic for topic in path["full_prerequisite_order"]
               if topic["id"] != target_id and topic["id"] not in set(path["already_learned"])]
    return {
        "target_topic": path["target_topic"],
        "missing_prerequisites": missing,
        "suggested_order": missing,
        "target_already_marked_learned": target_id in set(path["already_learned"]),
        "note": "Learned status is user-supplied and has not been independently assessed."
    }
