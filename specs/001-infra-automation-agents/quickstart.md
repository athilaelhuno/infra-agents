# Quickstart: Infra Automation Agents

## Prerequisites
- Python 3.11+
- Install dependencies: `pip install -r requirements.txt` (or via `uv`)
- Standard CLI tools installed: `terraform`, `terragrunt`, `kubectl`, `flux`, `glab`
- Authorized local sessions (e.g., `gcloud auth application-default login`, `glab auth login`)

## Environment Variables
Create a `.env` file at the root:
```env
# Optional LLM API keys depending on the provider you choose (e.g. OpenAI or Gemini)
OPENAI_API_KEY=your_key_here

JIRA_API_TOKEN=your_jira_token
CONFLUENCE_API_TOKEN=your_confluence_token
```

## Running the Orchestrator
To start the multi-agent system in interactive mode:
```bash
python src/orchestrator.py --interactive
```

To run a single prompt:
```bash
python src/orchestrator.py prompt "Por favor haz un terraform plan en el modulo de network y si esta ok dime que cambia."
```
