import pytest
from core.mapping import validate_topic_map, build_learning_path, identify_prerequisite_gaps

def sample():
    return {"target_topic": "c", "learned_topics": ["a"], "topics": [
        {"id": "a", "name": "A", "prerequisites": []},
        {"id": "b", "name": "B", "prerequisites": ["a"]},
        {"id": "c", "name": "C", "prerequisites": ["b"]}
    ]}

def test_validation_passes():
    assert validate_topic_map(sample())["valid"] is True

def test_learning_path_is_prerequisite_first():
    path = build_learning_path(sample(), "c")
    assert [x["id"] for x in path["full_prerequisite_order"]] == ["a", "b", "c"]

def test_learned_topics_filtered():
    path = build_learning_path(sample(), "c")
    assert [x["id"] for x in path["recommended_learning_path"]] == ["b", "c"]

def test_gap_analysis_excludes_target_from_prerequisites():
    gaps = identify_prerequisite_gaps(sample(), "c")
    assert [x["id"] for x in gaps["missing_prerequisites"]] == ["b"]

def test_unknown_prerequisite_rejected():
    data = sample()
    data["topics"][1]["prerequisites"] = ["missing"]
    with pytest.raises(ValueError):
        validate_topic_map(data)

def test_cycles_rejected():
    data = sample()
    data["topics"][0]["prerequisites"] = ["c"]
    with pytest.raises(ValueError):
        validate_topic_map(data)

def test_duplicate_topic_ids_rejected():
    data = sample()
    data["topics"].append({"id": "a", "name": "Duplicate", "prerequisites": []})
    with pytest.raises(ValueError):
        validate_topic_map(data)

def test_unknown_target_rejected():
    with pytest.raises(ValueError):
        build_learning_path(sample(), "unknown")
