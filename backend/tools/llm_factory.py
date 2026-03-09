"""
Factory de LLMs — OpenAI GPT-4o ou Google Gemini
"""
import os


def get_llm(provider: str = None):
    provider = provider or os.getenv("DEFAULT_LLM", "openai")

    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.7,
        )
    else:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model="gpt-4o",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7,
        )
