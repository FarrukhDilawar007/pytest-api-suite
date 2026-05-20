# Implementation Plan: pytest-api-suite

## Context
Build a complete production-quality REST API test suite from scratch against PetStore v2 (petstore.swagger.io/v2). The project is currently a skeleton (README only). Goal: demonstrate Python + pytest + Pydantic v2 + Pact contract testing + BDD patterns for a QA portfolio.

---

## Target API Summary (petstore.swagger.io/v2)

| Module | Endpoints |
|--------|-----------|
| Pet | POST /pet, PUT /pet, GET /pet/{id}, DELETE /pet/{id}, GET /pet/findByStatus, GET /pet/findByTags, POST /pet/{id}/uploadImage |
| Store | GET /store/inventory, POST /store/order, GET /store/order/{id}, DELETE /store/order/{id} |
| User | POST /user, GET/PUT/DELETE /user/{username}, POST /user/createWithArray, POST /user/createWithList, GET /user/login, GET /user/logout |

Auth: `api_key: special-key` header (required for GET /pet/{id} and GET /store/inventory).

---

## File Manifest (42 files)

### Config
- `requirements.txt`
- `pytest.ini` — markers, pythonpath, testpaths, strict-markers
- `conftest.py` — root fixtures

### src/
- `src/__init__.py`
- `src/models/__init__.py`
- `src/models/pet.py` — Pet, Category, Tag, ApiResponse (Pydantic v2)
- `src/models/store.py` — Order
- `src/models/user.py` — User
- `src/clients/__init__.py`
- `src/clients/base_client.py` — requests.Session, base URL, api_key header, retry, _request()
- `src/clients/pet_client.py`
- `src/clients/store_client.py`
- `src/clients/user_client.py`

### tests/pet/
- `tests/__init__.py`, `tests/pet/__init__.py`
- `tests/pet/test_pet_crud.py` — create, read, update, delete, 404, invalid ID
- `tests/pet/test_pet_upload_image.py`
- `tests/pet/test_pet_find_by_status.py` — parametrize available/pending/sold + invalid
- `tests/pet/test_pet_find_by_tags.py`

### tests/store/
- `tests/store/__init__.py`
- `tests/store/test_store_inventory.py`
- `tests/store/test_store_order_crud.py`
- `tests/store/test_store_order_negative.py`

### tests/user/
- `tests/user/__init__.py`
- `tests/user/test_user_crud.py`
- `tests/user/test_user_login_logout.py`
- `tests/user/test_user_create_array.py`
- `tests/user/test_user_create_list.py`

### tests/contract/
- `tests/contract/__init__.py`
- `tests/contract/consumer/__init__.py`
- `tests/contract/consumer/test_pet_consumer.py` — Pact mock server, GET/POST /pet
- `tests/contract/provider/__init__.py`
- `tests/contract/provider/mock_provider.py` — Flask app serving pet endpoints
- `tests/contract/provider/test_pet_provider.py` — Pact verifier against Flask mock

### tests/bdd/
- `tests/bdd/__init__.py`
- `tests/bdd/conftest.py` — BDD fixtures + all step definitions
- `tests/bdd/test_pet.py` — `scenarios('features/pet_lifecycle.feature')`
- `tests/bdd/test_user.py` — `scenarios('features/user_management.feature')`
- `tests/bdd/features/pet_lifecycle.feature` — 3 scenarios: create, update, delete
- `tests/bdd/features/user_management.feature` — 2 scenarios: create user, login

### CI
- `.github/workflows/ci.yml`

### Docs
- `README.md` — full rewrite per portfolio template

---

## Architecture Decisions

### BaseClient
```
BaseClient(base_url, api_key)
  Session with:
    - default headers: {"api_key": api_key, "Content-Type": "application/json"}
    - HTTPAdapter with Retry(total=3, backoff_factor=0.3, status_forcelist=[500, 502, 503])
  _request(method, path, **kwargs) → Response
    - calls session.request()
    - raises HTTPError on 4xx/5xx (tests assert on raised exception or raw response as needed)
```

Domain clients inherit BaseClient and add endpoint methods returning Pydantic models on success.

### Models (Pydantic v2)
- Use `model_validate()` (not `parse_obj`)
- All fields optional except `name` and `photoUrls` on Pet (matching spec)
- `ApiResponse` for upload endpoint

### conftest.py (root) Fixtures
| Fixture | Scope | Purpose |
|---------|-------|---------|
| `base_url` | session | "https://petstore.swagger.io/v2" |
| `api_key` | session | "special-key" |
| `pet_client` | session | PetClient instance |
| `store_client` | session | StoreClient instance |
| `user_client` | session | UserClient instance |
| `unique_id` | function | `random.randint(1_000_000, 9_999_999)` |
| `unique_pet` | function | creates pet → yields Pet → deletes in teardown |
| `unique_user` | function | creates user → yields dict → deletes in teardown |

### Test Markers
- `smoke` — on happy-path tests (create, read); runs on every PR
- `regression` — on all tests; runs on merge to main  
- `contract` — Pact tests only
- `bdd` — BDD scenarios only

### Negative Testing Strategy
- Call client methods that don't raise on 4xx (pass `raise_on_error=False` or call raw `_request`)
- Assert `response.status_code == 404` / `400` directly
- Don't go through Pydantic model validation for error responses

### Contract Testing (pact-python 1.x)
**Consumer** (`test_pet_consumer.py`):
1. Start pact mock server on localhost:1234
2. Define two interactions: `GET /pet/{id}` and `POST /pet`
3. Client hits mock server; pact verifies expectations are met
4. Pact JSON written to `pacts/` dir

**Provider** (`mock_provider.py` + `test_pet_provider.py`):
1. Flask app implements `/pet/<id>` GET and `/pet` POST with canned responses
2. Provider test spins up Flask on a free port, runs Pact verifier against it

### BDD (pytest-bdd v7)
- `test_pet.py` and `test_user.py` each call `scenarios(...)` — auto-generates one test per scenario
- All `@given/@when/@then` steps live in `tests/bdd/conftest.py` (pytest-bdd auto-collects from conftest)
- Steps share the same `pet_client` / `user_client` fixtures via injection

### CI (GitHub Actions)
```yaml
on: [push, pull_request]
jobs:
  smoke:         # always — pytest -m smoke
  regression:    # on main — pytest -m "not contract and not bdd"
  bdd:           # on main — pytest -m bdd
  contract:      # on main — pytest -m contract
  report:        # on main — upload allure-results artifact
```

---

## Test Coverage Matrix

| File | # Tests | Markers |
|------|---------|---------|
| test_pet_crud.py | 8 | smoke(3), regression |
| test_pet_find_by_status.py | 4 | regression (3 parametrized + 1 negative) |
| test_pet_find_by_tags.py | 2 | regression |
| test_pet_upload_image.py | 1 | regression |
| test_store_inventory.py | 2 | smoke(1), regression |
| test_store_order_crud.py | 3 | smoke(1), regression |
| test_store_order_negative.py | 3 | regression |
| test_user_crud.py | 6 | smoke(2), regression |
| test_user_login_logout.py | 3 | smoke(1), regression |
| test_user_create_array.py | 1 | regression |
| test_user_create_list.py | 1 | regression |
| test_pet_consumer.py | 2 | contract |
| test_pet_provider.py | 1 | contract |
| test_pet.py (BDD) | 3 | bdd |
| test_user.py (BDD) | 2 | bdd |
| **Total** | **~42** | |

---

## Implementation Order
1. requirements.txt + pytest.ini
2. src/models/ (Pet, Order, User)
3. src/clients/ (BaseClient → PetClient, StoreClient, UserClient)
4. conftest.py (root)
5. tests/pet/ (all 4 files)
6. tests/store/ (all 3 files)
7. tests/user/ (all 4 files)
8. tests/contract/ (consumer + provider)
9. tests/bdd/ (features + steps)
10. .github/workflows/ci.yml
11. README.md

## Verification
```bash
pip install -r requirements.txt
pytest -m smoke -v                  # ~15 tests, all green
pytest -m regression -v             # ~35 tests
pytest -m contract -v               # 3 contract tests
pytest -m bdd -v                    # 5 BDD scenarios
flake8 src/ tests/                  # no lint errors
```
