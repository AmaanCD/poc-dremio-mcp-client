
from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key is None:
            raise EnvironmentError("OpenAI API key is missing")






settings = Settings()