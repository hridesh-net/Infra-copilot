import requests

from typing import Any

from src.backend.agents.base import Agent
from src.backend.utils.llm_response import extract_llm_dict



GROQ_API_KEY = ""


class PromptGenerator(Agent):

    def __init__(self, config=None):
        super().__init__(config)

        self.inference = "GROQ"

        self.agent_prompt = (
            "You are an expert prompt engineer. "
            "Output valid JSON only, with exactly one top-level key named "
            "`prompt`. Do NOT include any other keys, code fences, markdown, "
            "or extra text. Your response must begin with '{' and end with '}'."
        )

        self.llm_params = {
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "temperature": 0.2,
            "max_completion_tokens": 1024,
            "stream": False,
            "stop": None,
        }

    def observe(self, inputs: Any):
        """Takes User's base Prompts and Inputs

        Args:
            inputs (Dict): User Input's as Dictionary containing Prompt and other configs
            {
                prompt: str,
                platform: [AWS],
                other: dict
            }
        """

        usr_prompt = inputs.get("prompt", "")
        platform = inputs.get("platform", "AWS")
        other_config = inputs.get("other_config", {})

        return (usr_prompt, platform, other_config)

    def decide(self, observation: tuple[str, str, dict[str, Any]]):
        print("in decide")
        usr_prompt, platform, other_config = observation

        messages = [
            {"role": "system", "content": self.agent_prompt},
            {"role": "user", "content": usr_prompt},
        ]

        self.llm_params["messages"] = messages

        url = ""
        headers = {}

        if self.inference == "GROQ":
            url = "https://api.groq.com/openai/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            }

        return (url, headers, platform, other_config)

    def act(self, plan: tuple[str, dict]):
        url, headers, platform, other_config = plan
        try:
            resp = requests.post(url=url, headers=headers, json=self.llm_params)
        except Exception as e:
            print(f"srror: {e}")

        data = extract_llm_dict(resp.json())
        # return data

        return data, platform, other_config
