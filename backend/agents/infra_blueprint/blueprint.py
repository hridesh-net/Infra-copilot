import requests

from src.backend.agents.base import Agent
from src.backend.utils.llm_response import extract_llm_dict

GROQ_API_KEY = ""


class BlueprintGen(Agent):
    """
    Generates Blueprint for Infrastruture.
    And store them into run time cntext and in memory as well
    """

    def __init__(self, config=None):
        super().__init__(config)

        self.inference = "GROQ"

        self.agent_prompt = (
            "You are a cloud expert engineer And you Only Generate a Blueprint of Infrastructure in json from the prompt you get"
            " - Output should be valid JSON only,"
            " - valid JSON will be of following format"
            """```json{
  "prompt": "string",
  "timestamp": "ISO‑8601 string",
  "environment": {
    "name": "string",
    "region": "string",
    "provider": "string"
  },
  "variables": {
    "string": "any"
  },
  "resources": [
    {
      "type": "string",
      "name": "string",
      "properties": { "string": "any" },
      "dependsOn": ["string"],
      "environment": {
        "envVars": [
          {
            "name": "string",
            "valueFrom": {
              "secretManager": {
                "arn": "string",
                "jsonKey"?: "string",
                "versionStage"?: "string",
                "versionId"?: "string"
              }
            }
          }
        ]
      }
    }
  ],
  "outputs": {
    "string": {
      "value": "any",
      "description"?: "string"
    }
  },
  "metadata"?: {
    "author"?: "string",
    "description"?: "string",
    "version"?: "string"
  }
}```"""
    """output example:"""
    """```json{
  "prompt": "Deploy prod web app in us‑east‑1 container with DB credentials from Secrets Manager",
  "timestamp": "2025‑08‑05T16:45:00Z",
  "environment": {
    "name": "prod",
    "region": "us‑east‑1",
    "provider": "aws"
  },
  "variables": {
    "instanceCount": 3
  },
  "resources": [
    {
      "type": "AWS::SecretsManager::Secret",
      "name": "DBSecret",
      "properties": {
        "Name": "prod/dbCredentials",
        "Description": "Database user/pass"
      }
    },
    {
      "type": "AWS::ECS::TaskDefinition",
      "name": "WebAppTask",
      "properties": {
        "family": "web‑app",
        "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecRole",
        "containerDefinitions": [
          {
            "name": "web",
            "image": "myorg/webapp:latest",
            "memory": 512,
            "cpu": 256,
            "secrets": [
              {
                "name": "DB_USERNAME",
                "valueFrom": "arn:aws:secretsmanager:us‑east‑1:123456789012:secret:prod/dbCredentials:username:AWSCURRENT:"
              },
              {
                "name": "DB_PASSWORD",
                "valueFrom": "arn:aws:secretsmanager:us‑east‑1:123456789012:secret:prod/dbCredentials:password:AWSCURRENT:"
              }
            ]
          }
        ]
      },
      "environment": {
        "envVars": [
          {
            "name": "DB_USER",
            "valueFrom": {
              "secretManager": {
                "arn": "arn:aws:secretsmanager:us‑east‑1:123456789012:secret:prod/dbCredentials",
                "jsonKey": "username",
                "versionStage": "AWSCURRENT"
              }
            }
          },
          {
            "name": "DB_PASS",
            "valueFrom": {
              "secretManager": {
                "arn": "arn:aws:secretsmanager:us‑east‑1:123456789012:secret:prod/dbCredentials",
                "jsonKey": "password",
                "versionStage": "AWSCURRENT"
              }
            }
          }
        ]
      },
      "dependsOn": ["DBSecret"]
    }
  ],
  "outputs": {
    "WebAppTaskArn": {
      "value": "${WebAppTask.Arn}",
      "description": "ARN of ECS Task definition"
    }
  },
  "metadata": {
    "author": "infra-agent-v2",
    "version": "2.0",
    "description": "Provision ECS task with DB creds from Secrets Manager"
  }
}```"""
" - Do NOT include any other keys, code fences, markdown, or Cloudformation Scripts "
            "or extra text. Your response must begin with '{' and end with '}'."
        )

        self.llm_params = {
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "temperature": 0.2,
            "max_completion_tokens": 1024,
            "stream": False,
            "stop": None,
        }


    def observe(self, inputs):
        """Takes refined Prompt and inputs
        Args:
            inputs (Dict): System Input's as Dictionary containing Prompt and other configs
            {
                prompt: str,
                platform: [AWS],
                other: dict
            }
        """

        ref_prompt = inputs.get("prompt", "")
        platform = inputs.get("platform", "AWS")
        other_config = inputs.get("other_config", {})

        return (ref_prompt, platform, other_config)

    def decide(self, observation):
        usr_prompt, platform, other_config = observation

        messages = [
            {"role": "system", "content": self.agent_prompt},
            {"role": "user", "content": usr_prompt},
        ]

        print(f"here is message {messages}")

        self.llm_params["messages"] = messages

        print(f"llm params: {self.llm_params}")

        url = ""
        headers = {}

        if self.inference == "GROQ":
            url = "https://api.groq.com/openai/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            }

        return (url, headers, platform, other_config)

    def act(self, plan):
        url, headers, platform, other_config = plan
        try:
            resp = requests.post(url=url, headers=headers, json=self.llm_params)
        except Exception as e:
            print(f"srror: {e}")

        print("--------- this i need ------")
        print(resp.json())

        data = extract_llm_dict(resp.json())
        # return data

        return data, platform, other_config
