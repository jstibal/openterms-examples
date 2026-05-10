# openterms-examples

Minimal examples showing how to use [OpenTerms](https://openterms.com) with the core Python SDK, LangChain, and CrewAI.

Every example runs without hitting any live API.

## What is OpenTerms?

OpenTerms is a machine-readable permissions protocol for the agentic web. Services publish an `openterms.json` file that describes what automated agents are and are not allowed to do. Agents read that file before acting.

```json
{
  "version": "1.0",
  "service": "example-service",
  "permissions": {
    "read_content": { "status": "allowed" },
    "scrape_data": { "status": "denied" },
    "api_access": { "status": "not_specified" }
  }
}
```

Agents check a key, get back a decision, and proceed only if the decision is `allow`.

## Structure

```text
openterms-examples/
├── examples/
├── fixtures/
└── tests/
```

## Fail-Closed Model

Default behavior: block unless explicitly allowed.

| OpenTerms status | Strict mode default | Permissive mode opt-in |
|---|---|---|
| `allowed` | Proceed | Proceed |
| `denied` | Block | Block |
| `not_specified` | Block | Proceed |
| `conditional` | Block | Proceed |
| key absent | Block | Proceed |

Permissive mode must always be an explicit opt-in. It is never the default.

## Canonical Permission Keys

| Key | What it covers |
|---|---|
| `read_content` | Reading or parsing public content |
| `scrape_data` | Structured data extraction or crawling |
| `api_access` | Calling the service API programmatically |
| `create_account` | Registering accounts or identities |
| `make_purchases` | Executing transactions |
| `post_content` | Submitting or publishing content |
| `allow_training` | Using content for ML model training |

## Registry Records Disclaimer

Registry records are informational records. Treat them as one input to agent decision logic.

## Installation

```bash
pip install "openterms-py>=0.3.1"
```

Optional integrations:

```bash
pip install langchain-openterms
pip install crewai-openterms
```

## Running the Examples

```bash
python examples/core_sdk_minimal.py
python examples/core_sdk_fail_closed.py
python examples/mock_openterms_json.py
python -m pytest tests/ -v
```

## Links

- OpenTerms homepage: https://openterms.com
- OpenTerms developer docs: https://openterms.com/sdk
- OpenTerms specification: https://openterms.com/docs
- openterms-py on PyPI: https://pypi.org/project/openterms-py/
- langchain-openterms on GitHub: https://github.com/jstibal/langchain-openterms
- crewai-openterms on GitHub: https://github.com/jstibal/crewai-openterms
