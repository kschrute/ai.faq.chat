import time
import uuid
from typing import Literal

from pydantic import BaseModel


class ChatCompletionMessage(BaseModel):
    """OpenAI chat completion message format."""

    role: Literal["assistant", "user", "system"]
    content: str | None


class ChatCompletionChoice(BaseModel):
    """OpenAI chat completion choice format."""

    index: int
    message: ChatCompletionMessage
    finish_reason: Literal["stop", "length", "content_filter", "null"]


class Usage(BaseModel):
    """OpenAI token usage information."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    """OpenAI chat completion response format."""

    id: str
    object: Literal["chat.completion"]
    created: int
    model: str
    choices: list[ChatCompletionChoice]
    usage: Usage


def build_chat_completion_response(
    content: str | None = None,
) -> ChatCompletionResponse:
    """
    Build a response in OpenAI chat completion format.

    Args:
        content: The answer content. If None, returns a response with null content.

    Returns:
        A ChatCompletionResponse in OpenAI chat.completion format.
    """
    return ChatCompletionResponse(
        id=f"chatcmpl-{uuid.uuid4().hex[:12]}",
        object="chat.completion",
        created=int(time.time()),
        model="faq-chat",
        choices=[
            ChatCompletionChoice(
                index=0,
                message=ChatCompletionMessage(role="assistant", content=content),
                finish_reason="stop",
            )
        ],
        usage=Usage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
    )
