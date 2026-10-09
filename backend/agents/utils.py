import os
import json
from typing import Any

def get_llm(model_name: str = "gpt-4o-mini", temperature: float = 0.2) -> Any:
    """
    Returns an initialized LLM instance.
    Prefers OpenAI ChatOpenAI if OPENAI_API_KEY is set or default,
    otherwise falls back to ChatGoogleGenerativeAI if GEMINI_API_KEY is set.
    """
    openai_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")

    if gemini_key and not openai_key:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            gemini_model = "gemini-1.5-flash" if "mini" in model_name else "gemini-1.5-pro"
            return ChatGoogleGenerativeAI(model=gemini_model, temperature=temperature)
        except Exception:
            pass

    from langchain_openai import ChatOpenAI
    return ChatOpenAI(model=model_name, temperature=temperature)

def parse_json_response(content: str) -> Any:
    """
    Cleans and parses a JSON response from an LLM call.
    Handles responses wrapped in markdown code blocks like ```json ... ```.
    """
    text = content.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    
    # In case there is still markdown prefix e.g. json\n{...}
    if text.startswith("json"):
        text = text[4:].strip()
        
    return json.loads(text)
