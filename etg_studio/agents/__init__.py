from .base_agent import BaseAgent
from .mock_agents import MockGeminiAgent, MockClaudeAgent, MockChatGPTAgent


def _lazy_import(name):
    """Lazy import per evitare errori se le dipendenze API non sono installate."""
    import importlib
    try:
        module = importlib.import_module(f".{name}", package=__name__)
        return module
    except ImportError:
        return None


def __getattr__(name):
    """Lazy loading degli agenti reali (richiedono librerie API)."""
    if name == "GeminiAgent":
        mod = _lazy_import("gemini_agent")
        if mod:
            return mod.GeminiAgent
        raise ImportError("google-generativeai non installato. Usa --demo o installa: pip install google-generativeai")
    if name == "ClaudeAgent":
        mod = _lazy_import("claude_agent")
        if mod:
            return mod.ClaudeAgent
        raise ImportError("anthropic non installato. Usa --demo o installa: pip install anthropic")
    if name == "ChatGPTAgent":
        mod = _lazy_import("chatgpt_agent")
        if mod:
            return mod.ChatGPTAgent
        raise ImportError("openai non installato. Usa --demo o installa: pip install openai")
    raise AttributeError(f"module 'agents' has no attribute {name!r}")
