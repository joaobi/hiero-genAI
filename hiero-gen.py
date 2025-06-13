"""
Hiero-Gen: Generate hand-written style images of Ancient Egyptian hieroglyphs
using Azure OpenAI's image API.

Requirements:
- python-dotenv
- requests

Usage:
    python hiero-gen.py
"""

import os
import base64
import requests
from dotenv import load_dotenv


class Config:
    """Handles loading and accessing environment variables."""

    def __init__(self):
        load_dotenv()
        self.endpoint = os.environ.get("AZURE_OPENAI_GPTIMAGE1_ENDPOINT")
        self.api_key = os.environ.get("AZURE_OPENAI_GPTIMAGE1_API_KEY")
        self.image_dir = os.path.join(os.curdir, "images")
        self._validate()

    def _validate(self):
        if not self.endpoint or not self.api_key:
            raise EnvironmentError(
                "Missing required environment variables: "
                "AZURE_OPENAI_GPTIMAGE1_ENDPOINT and/or AZURE_OPENAI_GPTIMAGE1_API_KEY"
            )


class ImageGenerator:
    """Handles image generation and saving."""

    def __init__(self, config: Config):
        self.config = config

    def generate_image(self, prompt: str, input_filename: str, output_filename: str) -> str:
        """
        Sends a request to the Azure OpenAI API to generate an image.

        Args:
            prompt (str): The prompt for image generation.
            input_filename (str): Path to the input image file.
            output_filename (str): Name for the output image file.

        Returns:
            str: Path to the saved image.
        """
        headers = {"api-key": self.config.api_key}
        files = {
            "image": (input_filename, open(input_filename, "rb"), "image/jpeg"),
            "prompt": (None, prompt),
            "quality": (None, "low"),
            "size": (None, "1024x1024"),
            "n": (None, "1"),
        }

        try:
            response = requests.post(
                self.config.endpoint, headers=headers, files=files, timeout=60
            )
            response.raise_for_status()
            result = response.json()
        except requests.RequestException as exc:
            raise RuntimeError(f"API request failed: {exc}") from exc
        finally:
            files["image"][1].close()

        return self._save_image(result, output_filename)

    def _save_image(self, result: dict, output_filename: str) -> str:
        """Decodes and saves the base64 image to disk."""
        os.makedirs(self.config.image_dir, exist_ok=True)
        image_path = os.path.join(self.config.image_dir, output_filename)
        try:
            b64_image = result["data"][0]["b64_json"]
            image_bytes = base64.b64decode(b64_image)
            with open(image_path, "wb") as f:
                f.write(image_bytes)
        except (KeyError, IndexError, base64.binascii.Error) as exc:
            raise RuntimeError("Failed to decode or save the image.") from exc
        return image_path


def main():
    """Main workflow for generating a hand-written style hieroglyph image."""
    prompt = (
        "I have attached a font version of an Ancient Egyptian hieroglyph sign."
        "Create a copy that looks like it was hand-written but stays close to the original as it still needs to represent the same sign."
        "Please make sure you keep all details the same."
    )
    input_filename = "A1.jpeg"
    output_filename = "A1.png"

    try:
        config = Config()
        generator = ImageGenerator(config)
        image_path = generator.generate_image(prompt, input_filename, output_filename)
        print(f"Image saved to {image_path}")
    except Exception as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
