from __future__ import annotations

import os
from functools import lru_cache

import boto3
import instructor

from models import PopulateResult
from prompts import SYSTEM_PROMPT


@lru_cache(maxsize=1)
def _get_client():
    env = os.environ.get("ENVIRONMENT", "dev").lower()
    if env == "dev":
        session = boto3.Session(
            profile_name=os.environ.get("AWS_PROFILE", "default")
        )
    else:
        session = boto3.Session()

    bedrock = session.client(
        "bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )
    return instructor.from_bedrock(bedrock)


def populate_template(conversation_history: str) -> PopulateResult:
    """Send conversation history to the LLM and return a structured result.

    Returns PopulateResult with either:
    - completed=True + template (all fields extracted)
    - completed=False + questions (missing info to ask the parent)
    """
    client = _get_client()
    model_id = os.environ.get(
        "BEDROCK_MODEL_ID", "us.anthropic.claude-sonnet-4-20250514-v1:0"
    )

    return client.messages.create(
        model=model_id,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": conversation_history},
        ],
        inferenceConfig={
            "maxTokens": 1024,
            "temperature": 0.0,
        },
        response_model=PopulateResult,
        max_retries=2,
    )
