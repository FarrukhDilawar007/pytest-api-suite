import pytest
from pytest_bdd import scenarios

pytestmark = pytest.mark.bdd

scenarios("features/user_management.feature")
