# GPT Dynamic Toolchain Builder

## Description
The GPT Dynamic Toolchain Builder is a Python library designed to help AI developers dynamically create and test GPT-5.5-compatible toolchains. Users can define custom tools and workflows using JSON specifications, which are then validated, integrated, and executed. This tool simplifies the prototyping and testing of workflows for tools leveraging GPT-5.5.

## Features
- **Dynamic Toolchain Creation**: Define custom tools and workflows using JSON specifications.
- **Seamless GPT-5.5 Integration**: Easily integrate with GPT-5.5 for executing workflows.
- **Simulation and Debug Mode**: Built-in simulation for testing toolchains without actual API calls.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd gpt_dynamic_toolchain
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Create a JSON file (e.g., `toolchain.json`) defining your tools and workflow. Example:

   ```json
   {
       "tools": [
           {
               "name": "tool1",
               "description": "A test tool",
               "parameters": {
                   "param1": "value1"
               }
           }
       ],
       "workflow": [
           {
               "tool": "tool1",
               "input": {
                   "param1": "value1"
               }
           }
       ]
   }
   ```

2. Run the tool:
   ```bash
   python -m gpt_dynamic_toolchain --config toolchain.json
   ```

3. View the output:
   ```json
   {
       "outputs": [
           {
               "tool": "tool1",
               "output": {
                   "simulated_output": "Executed tool1 with input {'param1': 'value1'}"
               }
           }
       ]
   }
   ```

## Testing

Run the tests using pytest:
```bash
pytest test_gpt_dynamic_toolchain.py
```

## License
This project is licensed under the MIT License.
