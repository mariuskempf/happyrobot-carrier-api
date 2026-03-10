# HappyRobot — Inbound Carrier Sales API

A FastAPI backend service that powers an AI-driven inbound carrier sales agent built on the [HappyRobot](https://happyrobot.ai) platform. The agent handles inbound calls from freight carriers looking to book loads — verifying their eligibility, matching them to available loads, and negotiating rates automatically.

## Overview

The API serves as the brain behind the voice agent. HappyRobot calls these endpoints mid-conversation to:

- **Verify carriers** via the FMCSA API (MC or DOT number)
- **Search and retrieve loads** from a seeded SQLite database

```
Carrier calls in → HappyRobot agent → FastAPI endpoints → Agent uses retrieved information & responds
```

## Architecture

```bash
happyrobot-carrier-api/
├── app/
│   ├── clients/           # FMCSA API client
│   ├── core/              # Config, security, logging
│   ├── routers/           # API endpoints
│   │   ├── carriers.py    # GET /carriers/verify/mc/{mc_number}
│   │   └── loads.py       # GET /loads/search, GET /loads/{load_id}
│   ├── app.py             # FastAPI application setup
│   ├── schemas.py         # Pydantic models
│   └── database.py        # SQLite helpers
├── data/
│   └── loads.db           # Pre-seeded load data (bundled in container)
├── docs/                  # Additional documentation
├── infrastructure/
│   └── terraform/         # Azure infrastructure as code
├── scripts/               # Utility scripts
├── tests/                 # Unit tests
├── .github/
│   └── workflows/         # CI/CD pipelines (ci.yaml, deploy.yaml)
├── example.env            # Environment variable reference
├── pyproject.toml         # Project dependencies
└── Dockerfile
```

## Local Development

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- Docker (optional, for container testing)

### Setup

1. Clone the repository and install dependencies

   ```bash
   git clone https://github.com/your-username/happyrobot-carrier-api
   cd happyrobot-carrier-api
   uv sync
   ```

2. Configure environment variables

   ```bash
   cp example.env .env
   # Fill in your values
   ```

3. Run the development server

   ```bash
   uv run python -m app
   ```

   The API will be available at `http://localhost:8000`. Swagger UI at `http://localhost:8000/docs`.

### Running with Docker

```bash
docker build -t happyrobot-carrier-api .
docker run --env-file .env -p 8000:8000 happyrobot-carrier-api
```

### Running Tests

```bash
uv run pytest tests
```

## API Reference

All endpoints (except `/health` and `/ready`) require authentication via the `Authorization` header:

```bash
Authorization: ApiKey <your-api-key>
```

| Method | Endpoint                            | Description                           |
| ------ | ----------------------------------- | ------------------------------------- |
| `GET`  | `/health`                           | Health check                          |
| `GET`  | `/ready`                            | Readiness check                       |
| `GET`  | `/carriers/verify/mc/{mc_number}`   | Verify carrier by MC number           |
| `GET`  | `/carriers/verify/dot/{dot_number}` | Verify carrier by DOT number          |
| `GET`  | `/loads/search`                     | Search available loads                |
| `GET`  | `/loads/find`                       | Find a single load by search criteria |
| `GET`  | `/loads/{load_id}`                  | Get load by ID                        |

## Environment Variables

| Variable          | Description                            | Required | Default                                             |
| ----------------- | -------------------------------------- | -------- | --------------------------------------------------- |
| `API_KEY`         | API key for endpoint authentication    | ✅       | —                                                   |
| `FMCSA__API_KEY`  | FMCSA API key for carrier verification | ✅       | —                                                   |
| `ENV`             | Environment name                       | ❌       | `dev`                                               |
| `LOG_LEVEL`       | Log level                              | ❌       | `INFO`                                              |
| `HOST`            | Host address to bind the server        | ❌       | `0.0.0.0`                                           |
| `PORT`            | Port to bind the server                | ❌       | `8000`                                              |
| `FMCSA__BASE_URL` | FMCSA API base URL                     | ❌       | `https://mobile.fmcsa.dot.gov/qc/services/carriers` |
| `FMCSA__TIMEOUT`  | FMCSA API request timeout (seconds)    | ❌       | `10.0`                                              |

## Deployment

See [docs/deployment.md](docs/deployment.md) for full cloud deployment instructions (Azure + Terraform + CI/CD).

## Database

See [docs/database.md](docs/database.md) for more info about the dummy database created. It holds the entries of available loads which can be queried via the `/loads` endpoints.
