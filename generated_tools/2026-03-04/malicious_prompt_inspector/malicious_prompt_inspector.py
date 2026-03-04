import argparse
import regex as re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

class MaliciousPromptInspector:
    def __init__(self):
        # Mock sentiment analyzer for testing purposes
        self.sentiment_analyzer = self.mock_sentiment_analyzer
        self.stop_words = set(stopwords.words('english'))

    def mock_sentiment_analyzer(self, prompt):
        """
        Mock sentiment analyzer to simulate behavior for testing.
        This should be replaced with a real model in production.
        """
        if "phishing" in prompt or "malware" in prompt:
            return [{"label": "NEGATIVE", "score": 0.9}]
        return [{"label": "POSITIVE", "score": 0.95}]

    def inspect_prompt(self, prompt):
        """
        Analyze a single prompt for malicious intent.

        Args:
            prompt (str): The input prompt to analyze.

        Returns:
            dict: A dictionary containing the classification and confidence score.
        """
        if not isinstance(prompt, str) or not prompt.strip():
            return {"classification": "invalid", "confidence": 0.0}

        # Tokenize and preprocess the prompt
        tokens = word_tokenize(prompt.lower())
        filtered_tokens = [word for word in tokens if word not in self.stop_words]

        # Check for suspicious keywords
        suspicious_keywords = ["phishing", "malware", "bypass", "hack", "exploit"]
        if any(keyword in filtered_tokens for keyword in suspicious_keywords):
            classification = "malicious"
            confidence = 0.9
        else:
            # Use sentiment analysis as a heuristic for suspicious content
            sentiment = self.sentiment_analyzer(prompt)[0]
            if sentiment['label'] == 'NEGATIVE' and sentiment['score'] > 0.8:
                classification = "suspicious"
                confidence = sentiment['score']
            else:
                classification = "safe"
                confidence = 1.0 - sentiment['score']

        return {"classification": classification, "confidence": round(confidence, 2)}

    def inspect_prompts(self, prompts):
        """
        Analyze a list of prompts for malicious intent.

        Args:
            prompts (list): A list of strings to analyze.

        Returns:
            dict: A dictionary with each prompt's classification and confidence score.
        """
        if not isinstance(prompts, list) or not all(isinstance(p, str) for p in prompts):
            raise ValueError("Input must be a list of strings.")

        return {prompt: self.inspect_prompt(prompt) for prompt in prompts}


def main():
    parser = argparse.ArgumentParser(description="Malicious Prompt Inspector")
    parser.add_argument("prompts", nargs="+", help="Prompts to analyze for malicious intent.")
    args = parser.parse_args()

    inspector = MaliciousPromptInspector()
    results = inspector.inspect_prompts(args.prompts)

    for prompt, result in results.items():
        print(f"Prompt: {prompt}\nClassification: {result['classification']}\nConfidence: {result['confidence']}\n")

if __name__ == "__main__":
    main()