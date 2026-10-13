# Explainability

## Inputs
The agent accepts a target topic ID, a list of topic records containing IDs, names, and prerequisite IDs, and an optional list of topic IDs the learner marks as learned.

## Decision
It validates the directed graph, traverses prerequisites before dependent topics, and returns a prerequisite-first sequence. Topics marked learned are excluded from the suggested study sequence. Missing prerequisite gaps are determined from the supplied graph and learned-topic list.

## Limits
The map is only as accurate as the supplied relationships. The agent does not independently assess mastery, retrieve curriculum standards, or determine universally correct prerequisites. Cycles and unknown references are rejected.

## Tool: validate-topic-map

### Inputs and Data Sources
A structured topic-map JSON object containing `topics`.

### Decision and Reasoning
Checks topic IDs, duplicate entries, prerequisite references, and cycles.

### Outputs and Evidence
Returns a validation summary based on the supplied graph.

### Limits and Constraints
Does not confirm whether the educational relationships are pedagogically correct.

### Failure Handling
Raises a clear ValueError for malformed topics, duplicate IDs, unknown references, or cycles.

### Human Review
A teacher or subject expert should confirm that prerequisite links are appropriate.

## Tool: build-learning-path

### Inputs and Data Sources
A validated topic map and a target topic ID.

### Decision and Reasoning
Uses depth-first traversal to list prerequisite topics before the target, then removes topics marked learned.

### Outputs and Evidence
Returns ordered topic IDs and names, plus the target topic.

### Limits and Constraints
A valid ordering is not a guarantee of optimal learning for every person.

### Failure Handling
Rejects unknown target IDs and invalid graph structures.

### Human Review
Learners and instructors should adapt the sequence to their goals and existing knowledge.

## Tool: identify-prerequisite-gaps

### Inputs and Data Sources
A validated topic map, target topic ID, and supplied learned-topic list.

### Decision and Reasoning
Finds prerequisite-chain topics absent from the learned-topic list.

### Outputs and Evidence
Returns missing topic records and a suggested order for addressing them.

### Limits and Constraints
Learned status is supplied by the user and is not independently assessed.

### Failure Handling
Rejects unknown targets and unknown learned-topic IDs.

### Human Review
Use quizzes or instructor feedback to check mastery where needed.
