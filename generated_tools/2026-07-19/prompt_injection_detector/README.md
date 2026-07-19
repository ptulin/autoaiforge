# Prompt Injection Detector

## Description
Prompt Injection Detector is a CLI tool designed to analyze LLM (Large Language Model) prompts for signs of malicious injections. It helps AI developers identify vulnerabilities in their prompt formulations by detecting common patterns of malicious behavior, providing risk scores, and offering suggestions to sanitize prompts.

## Features
- Detects common patterns of malicious prompt injections.
- Provides a risk score for input prompts.
- Offers actionable suggestions to sanitize vulnerable prompts.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/prompt_injection_detector.git
   cd prompt_injection_detector
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Analyze a Prompt
You can analyze a prompt by passing it as a command-line argument:

```bash
python prompt_injection_detector.py --prompt "Ignore previous instructions and do X"
```

### Example Output
```
Risk Score: 40
Suggestions:
- Avoid using phrases that override instructions.
- Rephrase the prompt to be more specific and constrained.
```

### Features
- **Risk Score:** A numerical representation (0-100) of the likelihood that the prompt contains malicious injections.
- **Suggestions:** Actionable recommendations to improve the prompt and reduce risks.

## Testing

Run the tests using `pytest`:

```bash
pytest test_prompt_injection_detector.py
```

## License
This project is licensed under the MIT License.