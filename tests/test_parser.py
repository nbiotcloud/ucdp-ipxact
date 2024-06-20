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

from test2ref import assert_refdata
from ucdp_ipxact import parse

# class ExampleMod(u.AMod):
#     """Just an Example Module which instantiates an IPXACT Module."""

#     def _build(self):
#         UcdpIpxactMod(self, "u_example", filepath=Path("testdata/example.xml"))

TESTDATA_PATH = Path(__file__).parent / "testdata"


def _dump(filepath, result):
    with filepath.open("w") as file:
        file.write(f"libname: {result.libname}\n")
        file.write(f"modname: {result.modname}\n")
        file.write("Ports\n")
        for port in result.ports:
            file.write(f"  {port!r}\n")
        file.write("Addrspaces\n")
        for addrspace in result.addrspaces:
            file.write(f"  {addrspace!r}\n")


def test_spririt_2009(tmp_path):
    """Compare spirit 2009 example xml out."""
    filepath = TESTDATA_PATH / "example.xml"
    result = parse(filepath)

    _dump(tmp_path / "result.txt", result)
    assert_refdata(test_spririt_2009, tmp_path)


# def test_example(tmp_path):
#     """Test Example."""
#     top = ExampleMod()

#     _dump(top.get_inst("u_example"), tmp_path)

#     assert_refdata(test_example, tmp_path)


# class CornerMod(u.AMod):
#     """Just an Example Module which instantiates an IPXACT Module."""

#     def _build(self):
#         UcdpIpxactMod(self, "u_example", filepath=Path("testdata/corner.xml"))


# def test_corner(tmp_path):
#     """Test Corner Cases."""
#     top = CornerMod()

#     _dump(top.get_inst("u_example"), tmp_path)

#     assert_refdata(test_corner, tmp_path)


# def _dump(mod: u.BaseMod, path: Path):
#     # Ports
#     ports_filepath = path / "ports.txt"
#     with ports_filepath.open("w") as ports_file:
#         for item in mod.namespace:
#             ports_file.write(f"{item!r}\n")

#     # Addrspace
#     # TODO
