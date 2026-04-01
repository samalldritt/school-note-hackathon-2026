# School Note Populator

API service that populates school absence note templates from parent conversations using an LLM (Claude on AWS Bedrock).

Sends conversation history to the model, which either returns a completed template or a list of follow-up questions to ask.

## Setup

### With Docker

```bash
docker compose up --build
```

### Without Docker

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uvicorn main:app --reload
```

### Environment Variables

Create a `.env` file in the project root:

```
ENVIRONMENT=dev
AWS_PROFILE=default
```

| Variable | Default | Description |
|---|---|---|
| `ENVIRONMENT` | `dev` | `dev` uses AWS profile auth, anything else uses default credentials |
| `AWS_PROFILE` | `default` | AWS CLI profile name (only used when `ENVIRONMENT=dev`) |
| `AWS_REGION` | `us-east-1` | Bedrock region |
| `BEDROCK_MODEL_ID` | `us.anthropic.claude-sonnet-4-20250514-v1:0` | Bedrock inference profile ID |

You need valid AWS credentials with Bedrock access configured via `aws configure` or SSO.

## API

### `POST /populate`

Send a conversation history string. Returns either a completed template or follow-up questions.

**Request:**

```json
{
  "conversation_history": "Parent: I need an absence note for my daughter Sarah Thompson. She is in 5th grade at Riverside Elementary. She had a fever and missed school on 2026-03-28. My name is David Thompson."
}
```

**Response (completed):**

```json
{
  "completed": true,
  "questions": null,
  "template": {
    "student_first_name": "Sarah",
    "student_last_name": "Thompson",
    "school_name": "Riverside Elementary",
    "grade": "5th",
    "absence_date": "2026-03-28",
    "reason": "Fever",
    "parent_guardian_name": "David Thompson",
    "additional_notes": null
  }
}
```

**Response (incomplete — needs more info):**

```json
{
  "completed": false,
  "questions": [
    "What is the student's last name?",
    "Which school does the student attend?"
  ],
  "template": null
}
```

### `GET /health`

Returns `{"status": "ok"}`.

## Integration

The orchestration service should loop:

1. Call `POST /populate` with the conversation so far
2. If `completed` is `false`, ask the returned `questions` to the parent and append their answers to the conversation string
3. Call `POST /populate` again with the updated conversation
4. Repeat until `completed` is `true`, then use the `template` object to generate the document
