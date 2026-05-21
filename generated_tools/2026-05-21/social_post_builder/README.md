# Social Media Post Builder

## Description
The Social Media Post Builder is a Python library and CLI tool that helps you generate engaging social media posts tailored for specific platforms, audiences, and tones. Powered by OpenAI's generative AI, this tool is perfect for creating posts for business marketing campaigns.

## Features
- Generate platform-specific social media posts (e.g., Twitter, LinkedIn, Facebook)
- Customize posts for different audience types (e.g., B2B, tech enthusiasts)
- Support for various tones (e.g., professional, casual, friendly)
- Option to batch-generate posts for campaigns

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/social_post_builder.git
   cd social_post_builder
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### CLI Example
Generate a post for Twitter:
```bash
python social_post_builder.py --platform "Twitter" --audience "tech enthusiasts" --message "new feature release"
```

Save the generated post to a file:
```bash
python social_post_builder.py --platform "LinkedIn" --audience "B2B" --message "launch new product" --output-file "post.txt"
```

### Library Example
Use the tool as a library in your Python code:
```python
from social_post_builder import generate_post

post = generate_post("Twitter", "tech enthusiasts", "casual", "new feature release")
print(post)
```

## Testing
Run the tests with pytest:
```bash
pytest test_social_post_builder.py
```

## Requirements
- Python 3.8+
- openai==0.27.0
- typer==0.9.0
- jinja2==3.1.2

## License
This project is licensed under the MIT License.