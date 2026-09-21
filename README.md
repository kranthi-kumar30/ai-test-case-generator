# AI Test Case Generator

A GenAI QA portfolio project that converts requirements, user stories, and acceptance criteria into structured software test cases.

## What this project demonstrates

- LLM-assisted test design
- Prompt engineering for QA workflows
- Positive, negative, boundary, validation, security, usability, and regression coverage
- Structured JSON output
- Streamlit UI
- Local fallback mode that works without API credentials
- Optional OpenAI or Azure OpenAI integration
- Automated tests

## Quick start

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install:

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run app.py
```

The app works immediately in Local Demo Mode.

## Optional LLM setup

Copy `.env.example` to `.env` and add your own OpenAI or Azure OpenAI credentials.

Never commit `.env` or real API keys.

## Suggested GitHub topics

`ai-testing` `llm-testing` `software-testing` `test-automation` `prompt-engineering` `quality-assurance` `generative-ai` `python` `streamlit`
