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
"""Test Command-Line-Interface."""

from click.testing import CliRunner
from pytest import fixture
from test2ref import assert_refdata
from ucdp.cli import ucdp


@fixture
def runner():
    """Click Runner for Testing."""
    yield CliRunner()


def _run(runner, path, cmd, exit_code=0):
    result = runner.invoke(ucdp, cmd)
    assert result.exit_code == exit_code
    (path / "console.txt").write_text(result.output.rstrip() + "\n")


def test_check(runner, tmp_path):
    """Check Command."""
    cmd = ["ipxact", "check", "tests/testdata/example-2009.xml"]
    _run(runner, tmp_path, cmd)
    assert_refdata(test_check, tmp_path)


def test_check_empty(runner, tmp_path):
    """Check Command on Empty File."""
    cmd = ["ipxact", "check", "tests/testdata/empty.xml"]
    _run(runner, tmp_path, cmd, exit_code=1)
    assert_refdata(test_check_empty, tmp_path)


def test_overview(runner, tmp_path):
    """Overview Command."""
    cmd = ["ipxact", "overview", "tests/testdata/example-2009.xml"]
    _run(runner, tmp_path, cmd)
    assert_refdata(test_overview, tmp_path)


def test_overview_empty(runner, tmp_path):
    """Overview Command on Empty File."""
    cmd = ["ipxact", "overview", "tests/testdata/empty.xml"]
    _run(runner, tmp_path, cmd, exit_code=1)
    assert_refdata(test_overview_empty, tmp_path)
