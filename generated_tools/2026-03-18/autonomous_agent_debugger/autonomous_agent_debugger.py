import argparse
import importlib.util
import os
import sys
import traceback
from rich.console import Console
from rich.prompt import Prompt
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

def load_agent(agent_path):
    """Dynamically load an agent script as a module."""
    if not os.path.exists(agent_path):
        raise FileNotFoundError(f"Agent script not found: {agent_path}")

    spec = importlib.util.spec_from_file_location("agent_module", agent_path)
    agent_module = importlib.util.module_from_spec(spec)
    sys.modules["agent_module"] = agent_module
    spec.loader.exec_module(agent_module)

    if not hasattr(agent_module, "run_agent") or not callable(agent_module.run_agent):
        raise AttributeError("Agent script must define a callable 'run_agent(task_input)' function.")

    return agent_module.run_agent

def debug_agent(agent_function, task_input):
    """Interactively debug an agent's execution."""
    console = Console()
    session = PromptSession()
    console.print("[bold green]Autonomous Agent Debugger[/bold green]")

    step = 0
    while True:
        try:
            console.print(f"\n[bold blue]Step {step}: Executing agent...[/bold blue]")
            output = agent_function(task_input)
            console.print("[bold yellow]Output:[/bold yellow]", output)

            action = session.prompt(
                "[bold cyan]Enter command ([n]ext, [q]uit): [/bold cyan]",
                completer=WordCompleter(["next", "quit"], ignore_case=True),
            )

            if action.lower() in ["q", "quit"]:
                console.print("[bold red]Exiting debugger.[/bold red]")
                break

            step += 1
        except Exception as e:
            console.print("[bold red]Error during execution:[/bold red]")
            console.print_exception()
            break

def main():
    parser = argparse.ArgumentParser(
        description="Autonomous Agent Debugger: Debug AI agent scripts interactively."
    )
    parser.add_argument(
        "--agent", required=True, help="Path to the Python script containing the agent."
    )
    parser.add_argument(
        "--task", required=True, help="Task input to provide to the agent."
    )

    args = parser.parse_args()

    try:
        agent_function = load_agent(args.agent)
        debug_agent(agent_function, args.task)
    except Exception as e:
        console = Console()
        console.print("[bold red]An error occurred:[/bold red]")
        console.print_exception()

if __name__ == "__main__":
    main()