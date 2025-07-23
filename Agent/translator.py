from config import load_config
from ollama import chat
from yaspin import yaspin

class Translator:
    def __init__(self):
        config = load_config()
        self.timeout = config.get("model_config", {}).get("timeout", 60)

        self.model = config.get("Model", "llama3")
        self.default_language = config.get("default_language", "en")
        self.name= config.get("assistant_name", "Assistant")
        

    def translate(
        self,
        text: str,
        src_lang: str = None,
        target_lang: str = None,
    ) -> str:
        src_lang = src_lang or self.default_language
        target_lang = target_lang or "en"
        prompt = (
            f"Translate the following text from {src_lang} to {target_lang} without further explanation.\n"
            "Find the best wording that match the original meanings"
            "Preserve formatting (like Markdown). Keep technical terms if needed"
            "Correct the user if there is any typo mistakes"
        )
        with yaspin(text="Translating...", color="cyan") as spinner:
            try:
                response = chat(
                    model=self.model,
                    messages=[
                        {'role': 'system', 'content': prompt},
                        {'role': 'user', 'content': text}
                    ],
                    think=False
                )
                spinner.ok("✓")
                return response['message']['content']

            except Exception as e:
                return f"[Translator_Error] {e}"