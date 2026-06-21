# Developer Agent Guide for octoDNS Akamai Edge DNS Provider

This repository contains the Akamai Edge DNS (formerly Fast DNS) provider for octoDNS. It enables planning, syncing, and applying DNS record states directly to Akamai's Edge DNS Zone Management API v2.

> [!IMPORTANT]
> **Core Workflow and Guidelines**
>
> All agents working on this repository must read and follow the general instructions and workflow guidelines defined in the core octoDNS `AGENTS.md` file.
> - **Local check**: Look for the file at `../octodns/AGENTS.md`.
> - **Remote check**: If the local file is not available, fetch it from GitHub: [octoDNS Core AGENTS.md](https://github.com/octodns/octodns/raw/refs/heads/main/AGENTS.md).
>
> You must align your code structure, style, pull request guidelines, and overall development workflows with the instructions specified there.

## Repository & Module Information

### Key Components

- **Provider Class**: [AkamaiProvider](file:///home/ross/octodns/octodns-edgedns/octodns_edgedns/__init__.py#L112-L696) (defined in [octodns_edgedns/__init__.py](file:///home/ross/octodns/octodns-edgedns/octodns_edgedns/__init__.py)). This is the primary provider mapping record representations.
- **Client Class**: [AkamaiClient](file:///home/ross/octodns/octodns-edgedns/octodns_edgedns/__init__.py#L26-L110) manages HTTP communication with the Akamai Fast DNS API.
- **Authentication**: Uses Akamai's proprietary EdgeGrid authorization mechanism (`EdgeGridAuth` from `akamai.edgegrid`) configured using:
  - `client_token`
  - `client_secret`
  - `access_token`
  - `host` (API endpoint host)

### Key Workflows & Features

1. **Supported Record Types**: `A`, `AAAA`, `AFSDB`, `CAA`, `CNAME`, `DNSKEY`, `DS`, `HINFO`, `LOC`, `MX`, `NAPTR`, `NS`, `PTR`, `RP`, `RRSIG`, `SPF`, `SRV`, `SSHFP`, `TXT`.
2. **Zone Comments**: Supports configuring changelog comments on zone records by utilizing the `comment` config option.
3. **Dynamic Routing**: Not supported (`SUPPORTS_DYNAMIC=False`, `SUPPORTS_GEO=False`).
4. **Dynamic Subnets**: Not supported (`SUPPORTS_DYNAMIC_SUBNETS=False`).
5. **Pool Value Status**: Not supported (`SUPPORTS_POOL_VALUE_STATUS=False`).

## Development & Testing

- **Setup Script**: Run `./script/bootstrap` to create a virtual environment, install dependencies (including `black`, `isort`, `pyflakes`, `akamai.edgegrid`, and `pytest`), and configure pre-commit hooks.
- **Test Suite**: Run unit tests using `pytest` via `./script/test` (or `pytest tests/`). Test files are located in [tests/](file:///home/ross/octodns/octodns-edgedns/tests).
- **Code Coverage**: Verify code coverage using `./script/coverage`.

## Key Constraints & Behaviors

- **Python Version**: Targets Python `>=3.9`.
- **Formatting**: Code formatting is enforced via `black` (version `>=26.0.0,<27.0.0`) and `isort`.
