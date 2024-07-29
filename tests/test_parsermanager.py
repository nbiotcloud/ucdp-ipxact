#
# MIT License
#
# Copyright (c) 2024 nbiotcloud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""Test Parser Manager."""

import re

from pytest import raises
from ucdp_ipxact.parsermanager import ParserManager


def test_basics():
    """Basic Testing."""
    parsermanager = ParserManager()
    assert len(parsermanager.parsers) == 0


def test_create():
    """Check Parser Manager Initialization."""
    parsermanager = ParserManager.create()
    assert len(parsermanager.parsers) == 1


def test_compatible():
    """Check Parser Manager is_compatible."""
    parsermanager = ParserManager.create()
    assert parsermanager.is_compatible("tests/testdata/example-2009.xml") is True
    assert parsermanager.is_compatible("tests/testdata/empty.xml") is False


def test_validate():
    """Check Parser Manager validate."""
    parsermanager = ParserManager.create()
    assert parsermanager.validate("tests/testdata/example-2009.xml") is True

    msg = "Unknown schema in"
    with raises(ValueError, match=re.escape(msg)):
        parsermanager.validate("tests/testdata/empty.xml")
