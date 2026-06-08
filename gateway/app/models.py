from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str
    content: str


# define the request model for gateway
class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    max_tokens: int = Field(default=128, ge=1, le=4096)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class BackendStatus(BaseModel):
    name: str
    base_url: str
    healthy: bool
    active_requests: int
