import json
import re
from typing import Any

def extract_llm_dict(response: dict[str, Any]) -> dict[str, Any]:
    """
    Given a chat-completion response dict, pull out the assistant's
    content, strip any ``` or ```json fences, and return it as a Python dict.

    Raises:
        KeyError, IndexError if expected fields are missing.
        json.JSONDecodeError if the stripped content is not valid JSON.
    """
    # 1) Pull out the raw content string
    print(f"here with data {response}")
    content = response["choices"][0]["message"]["content"].strip()
    print(f"conetent: {content}")

    # 2) Remove markdown code fences if present
    #    This covers both ```json ... ``` and ``` ... ```
    fence_pattern = r"^```(?:json)?\s*(.*)\s*```$"
    match = re.match(fence_pattern, content, flags=re.DOTALL)
    json_str = match.group(1) if match else content

    # 3) Parse and return
    return json.loads(json_str)
