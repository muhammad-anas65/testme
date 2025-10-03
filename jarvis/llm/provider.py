from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional

from openai import OpenAI

from ..config import settings

logger = logging.getLogger(__name__)


class OpenAIChatLLM:
    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY not configured")
        self.client = OpenAI(api_key=settings.openai_api_key)

    def chat(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        logger.debug("Sending chat completion with %d messages and %d tools", len(messages), 0 if not tools else len(tools))
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto" if tools else None,
            temperature=0.3,
        )
        choice = response.choices[0]
        message = choice.message
        result: Dict[str, Any] = {"role": message.role, "content": message.content}
        if message.tool_calls:
            # Normalize tool calls to a simple structure
            normalized = []
            for tc in message.tool_calls:
                try:
                    args = json.loads(tc.function.arguments or "{}")
                except json.JSONDecodeError:
                    args = {"raw": tc.function.arguments}
                normalized.append({
                    "id": tc.id,
                    "name": tc.function.name,
                    "arguments": args,
                })
            result["tool_calls"] = normalized
        return result
