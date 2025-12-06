# Universal Prompt Generator

Transform any user input into optimized, platform-specific AI prompts.

## Overview

The Universal Prompt Generator (UPG) analyzes your request and generates tailored prompts for multiple AI platforms:

- **ChatGPT** (OpenAI GPT-4)
- **Claude** (Anthropic) - with XML structure
- **Gemini** (Google)
- **Midjourney** - with proper parameters (--ar, --v, etc.)

## Quick Start

```bash
# Start all services
docker-compose up --build

# Test the API
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"input": "Write a professional email to my boss about requesting vacation next week"}'
```

## API

### Generate Prompts

```
POST /api/v1/generate
```

**Request:**
```json
{
  "input": "Write a professional email to my boss about vacation",
  "context": "I work at a tech startup",
  "platforms": ["chatgpt", "claude"],
  "options": {
    "include_assumptions": true
  }
}
```

**Response:**
```json
{
  "id": "upg_abc123def456",
  "input": "Write a professional email to my boss about vacation",
  "analysis": {
    "intent": "email_writing",
    "confidence": 0.92,
    "entities": [
      {"type": "recipient", "value": "boss"},
      {"type": "tone", "value": "professional"}
    ]
  },
  "prompts": {
    "chatgpt": {
      "prompt": "You are an expert email writer...",
      "placeholders": [
        {"key": "[RECIPIENT_NAME]", "description": "Name of the email recipient"}
      ],
      "settings": {"model": "gpt-4", "temperature": 0.7}
    },
    "claude": {
      "prompt": "<task>Write a professional email...</task>",
      "placeholders": [...],
      "settings": {"model": "claude-sonnet-4-20250514"}
    }
  },
  "placeholders": [
    {"name": "RECIPIENT_NAME", "description": "Name of recipient", "required": true}
  ],
  "assumptions": [
    {"category": "tone", "value": "Professional and formal tone", "reasoning": "Mentioned 'boss'"}
  ],
  "metadata": {
    "processing_time_ms": 145,
    "platforms_generated": ["chatgpt", "claude"],
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### List Platforms

```
GET /api/v1/platforms
```

### List Intents

```
GET /api/v1/intents
```

### Health Check

```
GET /health
GET /ready
```

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                 Core Service (Node.js)              │
│                   POST /api/v1/generate             │
│                      Port 8000                      │
└───────────────────────┬─────────────────────────────┘
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
┌─────────────────────┐     ┌─────────────────────┐
│  Analysis Service   │     │  Generation Service │
│      (Python)       │     │      (Python)       │
│     Port 8001       │     │     Port 8002       │
│                     │     │                     │
│ • Intent detection  │     │ • Template loading  │
│ • Entity extraction │     │ • Platform adapters │
│ • Assumptions       │     │ • Prompt rendering  │
└─────────────────────┘     └──────────┬──────────┘
                                       │
                                       ▼
                            ┌─────────────────────┐
                            │     PostgreSQL      │
                            │    (Templates)      │
                            └─────────────────────┘
```

## Supported Intents

| Intent | Description | Platforms |
|--------|-------------|-----------|
| `email_writing` | Professional/personal emails | ChatGPT, Claude, Gemini |
| `code_generation` | Code, scripts, functions | ChatGPT, Claude, Gemini |
| `image_generation` | AI image prompts | Midjourney |
| `summarization` | Content summarization | ChatGPT, Claude, Gemini |
| `translation` | Language translation | ChatGPT, Claude, Gemini |
| `creative_writing` | Stories, poems, creative content | ChatGPT, Claude, Gemini |

## Project Structure

```
universal-prompt-generator/
├── services/
│   ├── analysis-service/     # Python/FastAPI - NLU
│   ├── generation-service/   # Python/FastAPI - Prompt generation
│   └── core-service/         # Node.js/Express - Public API
├── templates/                # Prompt templates (YAML)
│   ├── chatgpt/
│   ├── claude/
│   ├── gemini/
│   └── midjourney/
├── docker-compose.yml
└── README.md
```

## Development

### Run Locally (without Docker)

**Analysis Service:**
```bash
cd services/analysis-service
pip install -r requirements.txt
uvicorn src.main:app --port 8001 --reload
```

**Generation Service:**
```bash
cd services/generation-service
pip install -r requirements.txt
uvicorn src.main:app --port 8002 --reload
```

**Core Service:**
```bash
cd services/core-service
npm install
npm run dev
```

### Environment Variables

| Variable | Service | Default | Description |
|----------|---------|---------|-------------|
| `PORT` | All | varies | Service port |
| `DATABASE_URL` | Generation | - | PostgreSQL connection string |
| `ANALYSIS_SERVICE_URL` | Core | http://localhost:8001 | Analysis service URL |
| `GENERATION_SERVICE_URL` | Core | http://localhost:8002 | Generation service URL |

## Adding New Platforms

1. Create adapter in `services/generation-service/src/core/adapters/`
2. Register in `registry.py`
3. Add templates in `templates/<platform>/`

Example adapter:
```python
from .base import BaseAdapter

class NewPlatformAdapter(BaseAdapter):
    platform_id = "new_platform"
    platform_name = "New Platform"
    platform_type = "text"
    
    supported_intents = ["email_writing", "code_generation"]
    
    def generate(self, analysis, template_content):
        # Your generation logic
        pass
    
    def apply_rules(self, prompt):
        # Platform-specific rules
        return prompt
```

## License

MIT