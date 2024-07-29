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
"""Test IPXACT Importing."""

from pathlib import Path

import ucdp as u
from pytest import raises
from test2ref import assert_refdata
from ucdp_ipxact import UcdpIpxactMod, parse, validate

TESTDATA_PATH = Path(__file__).parent / "testdata"


class Top2009Mod(u.AMod):
    """2009 Version."""

    def _build(self):
        UcdpIpxactMod(self, "u_inst0", filepath=Path("testdata/example-2009.xml"))
        UcdpIpxactMod(self, "u_inst1", filepath=Path("testdata/example-2009.xml"))


def test_missing_file(tmp_path):
    """Missing."""
    with raises(FileNotFoundError):
        validate(tmp_path / "missing.xml")


def test_validate_2009():
    """Validate 2009 Example Xml."""
    assert validate(TESTDATA_PATH / "example-2009.xml") is True


def test_parse_2009(tmp_path):
    """Parse 2009 Example Xml."""
    filepath = TESTDATA_PATH / "example-2009.xml"
    ipxact = parse(filepath)
    (tmp_path / "result.txt").write_text(ipxact.get_overview())
    assert_refdata(test_parse_2009, tmp_path)


def test_mod_2009(tmp_path):
    """2009 Example Module."""
    mod = Top2009Mod()

    inst0 = mod.get_inst("u_inst0")
    (tmp_path / "inst0.txt").write_text(inst0.get_overview())
    assert inst0.name == "u_inst0"
    assert inst0.modname == "VGA"
    assert inst0.libname == "user"
    assert len(tuple(inst0.get_addrspaces())) == 2

    inst1 = mod.get_inst("u_inst1")
    (tmp_path / "inst1.txt").write_text(inst1.get_overview())
    assert inst1.name == "u_inst1"
    assert inst1.modname == "VGA"
    assert inst1.libname == "user"
    assert len(tuple(inst1.get_addrspaces())) == 2

    assert_refdata(test_mod_2009, tmp_path)
