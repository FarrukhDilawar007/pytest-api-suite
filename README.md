# pytest-api-suite

Production-quality REST API test suite demonstrating Python + pytest + Pact contract testing + BDD — built against the PetStore v2 API.

## What this is

A complete API test automation framework covering full CRUD operations across three API modules (Pet, Store, User), consumer-driven contract testing with Pact, and BDD scenarios written in Gherkin. Demonstrates patterns used in enterprise QA: typed HTTP clients, Pydantic response validation, fixture-based teardown, and pytest marker-based CI gating.

## Stack

- **Python 3.11+** · **pytest 7.4+**
- **requests** — HTTP client with session reuse and retry
- **Pydantic v2** — response schema validation on every endpoint
- **pytest-bdd** — Gherkin BDD layer (business-readable scenarios)
- **Pact** — consumer-driven contract testing (consumer + Flask mock provider)
- **Allure** — rich HTML reports
- **GitHub Actions** — smoke gate on PR, full regression on merge to main

## Folder structure

```
pytest-api-suite/
├── src/
│   ├── clients/          # BaseClient (Session + retry) → PetClient, StoreClient, UserClient
│   └── models/           # Pydantic v2: Pet, Category, Tag, ApiResponse, Order, User
├── tests/
│   ├── pet/              # CRUD, findByStatus, findByTags, image upload
│   ├── store/            # Inventory, order CRUD, negative tests
│   ├── user/             # CRUD, login/logout, bulk create
│   ├── contract/
│   │   ├── consumer/     # Pact consumer definitions (writes pacts/ JSON)
│   │   └── provider/     # Flask mock provider + Pact verifier
│   └── bdd/
│       ├── features/     # Gherkin: pet_lifecycle.feature, user_management.feature
│       └── conftest.py   # All @given/@when/@then step definitions
├── conftest.py           # Shared fixtures: clients, unique_pet, unique_user
├── pytest.ini
└── .github/workflows/ci.yml
```

## How to run locally

**Prerequisites:** Python 3.11+

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Lint
flake8 src/ tests/ --max-line-length=120

# 3. Run smoke tests (fast, ~15 tests)
pytest -m smoke -v

# 4. Run full regression suite
pytest -m regression -v

# 5. Run BDD scenarios
pytest -m bdd -v

# 6. Run contract tests (requires pact-standalone binary — auto-downloaded)
pytest -m contract tests/contract/consumer/ -v  # generates pacts/
pytest -m contract tests/contract/provider/ -v  # verifies pacts/

# 7. Single file or test
pytest tests/pet/test_pet_crud.py -v
pytest tests/pet/test_pet_crud.py::test_create_pet -v

# 8. Generate HTML report
pytest -m regression --html=report.html --self-contained-html

# 9. Generate Allure report
pytest -m regression --alluredir=allure-results
allure serve allure-results
```

## CI

| Trigger | Job | Tests |
|---------|-----|-------|
| Every push / PR | **Smoke** | `pytest -m smoke` (~15 tests) |
| Merge to main | **Regression** | `pytest -m regression` (~35 tests) + BDD |
| Merge to main | **Contract** | Consumer pact generation + provider verification |
| Every push | **Lint** | `flake8 src/ tests/` |

Allure results are uploaded as a CI artifact on every regression run.

## Target API

[PetStore v2](https://petstore.swagger.io/v2) — Swagger's official sample REST API.  
API key: `special-key` (standard test key, no registration required).
