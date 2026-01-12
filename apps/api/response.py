import time
import uuid


def build_chat_completion_response(content: str | None = None) -> dict:
    """
    Build a response in OpenAI chat completion format.
    
    Args:
        content: The answer content. If None, returns a response with null content.
    
    Returns:
        A dictionary in OpenAI chat.completion format.
    """
    return {
        "id": f"chatcmpl-{uuid.uuid4().hex[:12]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "faq-chat",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": content
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
    }
