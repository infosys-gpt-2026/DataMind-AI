from typing import Dict, List, Optional

from fastapi import FastAPI # pyright: ignore[reportMissingImports]
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage

from agents.analyst_agent import analyst_agent_executor

app = FastAPI(
    title="DataMind AI API",
    description="HTTP interface for the DataMind AI tool-calling analyst agent.",
    version="1.0.0",
)

# Simple in-memory session store: session_id -> list of chat messages.
# Not persistent across restarts — fine for demos and n8n automation triggers,
# not a substitute for a real database if you need durable multi-user history.
_sessions: Dict[str, List] = {}


class AnalyzeRequest(BaseModel):
    question: str
    session_id: Optional[str] = "default"


class AnalyzeResponse(BaseModel):
    answer: str
    session_id: str


@app.get("/health")
def health() -> dict:
    """Simple liveness check — useful for n8n or uptime monitors to confirm the API is up."""
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """
    Ask DataMind AI a question. Pass the same session_id across calls to keep
    conversation memory (e.g. so 'load the CSV' then 'summarize it' works across
    two separate HTTP requests). Omit session_id to use the shared 'default' session.
    """
    history = _sessions.get(request.session_id, []) # pyright: ignore[reportCallIssue, reportArgumentType]

    result = analyst_agent_executor.invoke(
        {"question": request.question, "chat_history": history}
    )
    answer = _extract_text(result["output"])

    history.append(HumanMessage(content=request.question))
    history.append(AIMessage(content=answer))
    _sessions[request.session_id] = history # pyright: ignore[reportArgumentType]

    return AnalyzeResponse(answer=answer, session_id=request.session_id) # pyright: ignore[reportArgumentType]


@app.post("/reset")
def reset_session(session_id: str = "default") -> dict:
    """Clear a session's chat history — useful before starting a fresh analysis run."""
    _sessions.pop(session_id, None)
    return {"status": "reset", "session_id": session_id}
def _extract_text(output) -> str:
    """
    Normalize the agent's output into a plain string. Some Gemini responses come back
    as a list of content blocks (e.g. [{'type': 'text', 'text': '...'}]) instead of a
    plain string — this pulls the actual text out of that shape either way.
    """
    if isinstance(output, str):
        return output
    if isinstance(output, list):
        parts = []
        for block in output:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts).strip()
    return str(output)