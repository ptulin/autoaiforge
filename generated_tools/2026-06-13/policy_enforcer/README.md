# Policy Enforcer

Policy Enforcer is a lightweight Python library for defining and enforcing governance policies for AI agent actions. Developers can define rulesets (e.g., allowable actions, thresholds, or resource usage limits) and dynamically apply them to monitor and restrict agent behavior in production.

## Features

- Define custom policy rules for agent behavior.
- Cross-check agent actions against defined policies.
- Event-based triggers for violations, such as alerts or action rollbacks.

## Installation

Install the library using pip:

```bash
pip install -r requirements.txt
```

## Usage

### Example

```python
from policy_enforcer import PolicyEnforcer

rules = [
    {
        "name": "Limit action type",
        "condition": {"type": {"allowed": ["read", "write"]}},
        "message": "Action type not allowed"
    }
]

action = {"type": "delete"}

enforcer = PolicyEnforcer(rules)
result = enforcer.check(action)

print(result)
```

### CLI Usage

```bash
python policy_enforcer.py <rules.json> <action.json>
```

## Testing

Run tests using pytest:

```bash
pytest test_policy_enforcer.py
```
