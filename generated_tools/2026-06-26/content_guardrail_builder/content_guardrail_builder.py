import argparse
import yaml
import regex as re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

class ContentGuardrailBuilder:
    def __init__(self, config_path):
        self.config = self._load_config(config_path)
        self.ml_model = None
        if "ml_model" in self.config:
            self.ml_model = self._load_ml_model(self.config["ml_model"])

    def _load_config(self, config_path):
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            raise ValueError(f"Error loading configuration file: {e}")

    def _load_ml_model(self, model_config):
        try:
            training_data = model_config.get("training_data")
            labels = model_config.get("labels")
            if not training_data or not labels:
                raise ValueError("Missing training data or labels in ML model configuration.")

            vectorizer = CountVectorizer()
            model = MultinomialNB()
            pipeline = make_pipeline(vectorizer, model)
            pipeline.fit(training_data, labels)
            return pipeline
        except Exception as e:
            raise ValueError(f"Error loading ML model: {e}")

    def filter_content(self, content):
        diagnostics = []
        sanitized_content = content

        # Keyword filtering
        for keyword in self.config.get("keywords", []):
            if keyword in content:
                diagnostics.append(f"Keyword match: {keyword}")
                sanitized_content = sanitized_content.replace(keyword, "[REDACTED]")

        # Regex filtering
        for pattern in self.config.get("regex_patterns", []):
            matches = re.findall(pattern, content)
            if matches:
                diagnostics.append(f"Regex match: {pattern}")
                sanitized_content = re.sub(pattern, "[REDACTED]", sanitized_content)

        # ML model filtering
        if self.ml_model:
            prediction = self.ml_model.predict([content])[0]
            if prediction == 1:  # Assuming 1 indicates harmful content
                diagnostics.append("ML model flagged content as harmful.")
                sanitized_content = "[REDACTED]"

        return sanitized_content, diagnostics

    def process_file(self, content_path):
        try:
            with open(content_path, 'r') as file:
                content = file.read()
            return self.filter_content(content)
        except Exception as e:
            raise ValueError(f"Error reading content file: {e}")


def main():
    parser = argparse.ArgumentParser(description="Content Guardrail Builder")
    parser.add_argument("--config", required=True, help="Path to the configuration file (YAML format).")
    parser.add_argument("--content", required=True, help="Path to the content file to be filtered.")
    args = parser.parse_args()

    try:
        builder = ContentGuardrailBuilder(args.config)
        sanitized_content, diagnostics = builder.process_file(args.content)

        print("Sanitized Content:")
        print(sanitized_content)
        print("\nDiagnostics:")
        for diagnostic in diagnostics:
            print(f"- {diagnostic}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()