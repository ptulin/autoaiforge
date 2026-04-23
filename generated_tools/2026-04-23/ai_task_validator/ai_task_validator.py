import json
from typing import List, Dict, Any
from pydantic import BaseModel, ValidationError, root_validator
import networkx as nx

class Task(BaseModel):
    id: str
    dependencies: List[str] = []
    inputs: List[str] = []
    outputs: List[str] = []

    @root_validator
    def validate_task(cls, values):
        if values['id'] in values['dependencies']:
            raise ValueError(f"Task '{values['id']}' cannot depend on itself.")
        return values

def validate_tasks(task_definitions: List[Dict[str, Any]]) -> Dict[str, Any]:
    try:
        tasks = [Task(**task) for task in task_definitions]
    except ValidationError as e:
        return {"status": "error", "message": "Invalid task definitions.", "details": e.errors()}

    graph = nx.DiGraph()
    for task in tasks:
        graph.add_node(task.id)
        for dependency in task.dependencies:
            graph.add_edge(dependency, task.id)

    if not nx.is_directed_acyclic_graph(graph):
        cycles = list(nx.simple_cycles(graph))
        return {"status": "error", "message": "Circular dependencies detected.", "details": cycles}

    missing_dependencies = []
    for task in tasks:
        for dependency in task.dependencies:
            if dependency not in [t.id for t in tasks]:
                missing_dependencies.append({"task": task.id, "missing_dependency": dependency})

    if missing_dependencies:
        return {"status": "error", "message": "Missing dependencies found.", "details": missing_dependencies}

    optimization_suggestions = []
    for task in tasks:
        for output in task.outputs:
            dependent_tasks = [other_task for other_task in tasks if task.id != other_task.id and output in other_task.inputs]
            if len(dependent_tasks) > 1:
                if not any(
                    suggestion["task"] == task.id and suggestion["output"] == output
                    for suggestion in optimization_suggestions
                ):
                    optimization_suggestions.append({
                        "task": task.id,
                        "output": output,
                        "suggestion": f"Consider optimizing the output '{output}' to avoid redundancy."
                    })

    return {"status": "success", "message": "Tasks validated successfully.", "optimizations": optimization_suggestions}

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AI Task Validator")
    parser.add_argument("input_file", type=str, help="Path to the JSON file containing task definitions.")
    parser.add_argument("output_file", type=str, help="Path to save the validation report as JSON.")

    args = parser.parse_args()

    try:
        with open(args.input_file, "r") as f:
            task_definitions = json.load(f)

        result = validate_tasks(task_definitions)

        with open(args.output_file, "w") as f:
            json.dump(result, f, indent=4)

        print(f"Validation report saved to {args.output_file}")
    except Exception as e:
        print(f"Error: {e}")