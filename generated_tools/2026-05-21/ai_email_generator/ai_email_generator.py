import openai
import click
from pydantic import BaseModel, ValidationError, constr
import os

class EmailRequest(BaseModel):
    tone: constr(min_length=1)
    purpose: constr(min_length=1)
    key_points: constr(min_length=1)

    def to_prompt(self):
        return (
            f"Generate a {self.tone} email for the following purpose: {self.purpose}. "
            f"Include the following key points: {self.key_points}."
        )

def generate_email(api_key, email_request):
    openai.api_key = api_key

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=email_request.to_prompt(),
            max_tokens=300,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise RuntimeError(f"Failed to generate email: {e}")

@click.command()
@click.option('--tone', required=True, help='Tone of the email (e.g., formal, casual).')
@click.option('--purpose', required=True, help='Purpose of the email (e.g., follow-up, introduction).')
@click.option('--key_points', required=True, help='Key points to include in the email.')
@click.option('--output_file', default=None, help='File to save the generated email.')
def main(tone, purpose, key_points, output_file):
    """AI Email Generator: Generate professional-quality business emails."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        click.echo("Error: OPENAI_API_KEY environment variable is not set.")
        return

    try:
        email_request = EmailRequest(tone=tone, purpose=purpose, key_points=key_points)
        email_content = generate_email(api_key, email_request)

        if output_file:
            with open(output_file, 'w') as f:
                f.write(email_content)
            click.echo(f"Email saved to {output_file}")
        else:
            click.echo("Generated Email:")
            click.echo(email_content)

    except ValidationError as e:
        click.echo(f"Input validation error: {e}")
    except RuntimeError as e:
        click.echo(f"Error: {e}")

if __name__ == "__main__":
    main()
