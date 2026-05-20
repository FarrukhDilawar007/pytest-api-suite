"""
Pact provider verification test.

Spins up the Flask mock provider, then verifies it satisfies
every interaction defined in the consumer pact file.

Note: requires pact-python FFI (pact_ffi). On Windows with Python 3.13 the
DLL may fail to load — tests are skipped in that case and run in Linux CI.
"""
import threading
import time
import pytest

try:
    from pact import Verifier
    _PACT_AVAILABLE = True
except (ImportError, OSError):
    _PACT_AVAILABLE = False

from tests.contract.provider.mock_provider import app

pytestmark = pytest.mark.skipif(
    not _PACT_AVAILABLE,
    reason="pact-python FFI not available on this platform — runs in CI (Linux)",
)

PROVIDER_HOST = "localhost"
PROVIDER_PORT = 5050
PACT_FILE = "pacts/petconsumer-petprovider.json"


@pytest.fixture(scope="module")
def provider_server():
    server = threading.Thread(
        target=lambda: app.run(host=PROVIDER_HOST, port=PROVIDER_PORT, use_reloader=False),
        daemon=True,
    )
    server.start()
    time.sleep(1)
    yield


@pytest.mark.contract
def test_provider_satisfies_consumer_pact(provider_server):
    verifier = Verifier(  # noqa: F821 — guarded by pytestmark skipif above
        provider="PetProvider",
        provider_base_url=f"http://{PROVIDER_HOST}:{PROVIDER_PORT}",
    )
    output, _ = verifier.verify_pacts(PACT_FILE)
    assert output == 0, "Pact provider verification failed — consumer contract not satisfied"
