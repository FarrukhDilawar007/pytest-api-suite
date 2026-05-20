# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Status

**In progress** — skeleton only (README exists; no source yet). Full spec lives in `../PORTFOLIO-PLAN.md`. Implement according to that spec; do not invent scope beyond it.

## Commands

```bash
pip install -r requirements.txt
flake8 src/ tests/                                              # lint
pytest                                                          # all tests
pytest tests/pet/test_pet_crud.py                              # single file
pytest tests/pet/test_pet_crud.py::test_create_pet             # single test
pytest -m smoke                                                 # PR gate subset
pytest -m regression                                            # full suite
pytest -m contract                                              # Pact only
pytest -m bdd                                                   # BDD only
pytest --html=report.html                                       # HTML report
pytest --alluredir=allure-results                               # Allure report
```

Markers are declared in `pytest.ini`: `smoke`, `regression`, `contract`, `bdd`.

## Architecture

### Layer model

```
conftest.py              ← fixtures: api_key, unique_pet factory, cleanup
src/clients/
  base_client.py         ← requests.Session, base URL, auth headers, retry
  pet_client.py          ← /pet endpoints
  store_client.py        ← /store endpoints
  user_client.py         ← /user endpoints
src/models/
  pet.py                 ← Pydantic v2: Pet, Category, Tag, ApiResponse
  store.py               ← Pydantic v2: Order
  user.py                ← Pydantic v2: User
tests/pet/               ← CRUD, upload, findByStatus, findByTags
tests/store/             ← inventory, order CRUD, negatives
tests/user/              ← CRUD, login/logout, bulk create, negatives
tests/contract/
  consumer/              ← Pact consumer contract definitions
  provider/              ← Flask mock provider + Pact verification
tests/bdd/
  features/              ← Gherkin: pet_lifecycle.feature, user_management.feature
  steps/                 ← pytest-bdd step definitions
.github/workflows/
  ci.yml                 ← smoke on PR, full regression on merge to main
```

### Key design decisions

- **`base_client.py`** owns the `requests.Session`; domain clients (`pet_client.py` etc.) inherit from it and add only endpoint methods — no HTTP setup in domain clients.
- **Pydantic v2 models** validate every response; tests assert on model fields, not raw dicts.
- **`conftest.py` cleanup fixture** deletes all test-created resources after each test — tests must not leave data in the live PetStore API.
- **No `time.sleep`** anywhere — use `pytest` retry logic or explicit polling if needed.
- Contract tests use **Pact** (consumer-driven): consumer defines expectations, Flask mock provider verifies them independently.

## Target API

PetStore v2 — `https://petstore.swagger.io/v2`. No auth required for most endpoints; `api_key` header used for delete operations.

## Tech stack

Python 3.11+, pytest, requests, Pydantic v2, pytest-bdd, pact-python, pytest-html / Allure.
