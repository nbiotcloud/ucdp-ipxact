"""Pytest Configuration and Fixtures."""

from pathlib import Path

import ucdp as u
import ucdp_ipxact
from pytest import fixture

EXAMPLES_PATH = Path(ucdp_ipxact.__file__).parent / "example"


@fixture
def example_simple():
    """Add access to ``examples/simple``."""
    example_path = EXAMPLES_PATH / "simple"
    with u.extend_sys_path((example_path,)):
        yield example_path
