import openai
import typer
from jinja2 import Template
from typing import Optional

def generate_post(platform: str, audience: str, tone: str, message: str) -> str:
    """Generates a social media post using OpenAI's API."""
    prompt_template = Template(
        """
        Write a {{ tone }} social media post for {{ platform }} targeting {{ audience }}. The key message is: "{{ message }}".
        """
    )

    prompt = prompt_template.render(platform=platform, audience=audience, tone=tone, message=message)

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise RuntimeError(f"Failed to generate post: {e}")

def main(
    platform: str = typer.Option(..., help="Platform for the post (e.g., Twitter, LinkedIn)"),
    audience: str = typer.Option(..., help="Target audience (e.g., B2B, tech enthusiasts)"),
    tone: str = typer.Option("professional", help="Tone of the post (e.g., professional, casual)"),
    message: str = typer.Option(..., help="Key message for the post"),
    output_file: Optional[str] = typer.Option(None, help="File to save the generated post")
):
    """CLI entry point for generating social media posts."""
    try:
        post = generate_post(platform, audience, tone, message)
        if output_file:
            with open(output_file, "w") as file:
                file.write(post)
            typer.echo(f"Post saved to {output_file}")
        else:
            typer.echo("Generated Post:")
            typer.echo(post)
    except RuntimeError as e:
        typer.echo(f"Error: {e}", err=True)

if __name__ == "__main__":
    typer.run(main)