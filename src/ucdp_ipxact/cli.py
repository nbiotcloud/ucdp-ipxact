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

"""Command Line Interface."""

from pathlib import Path

import click
from ucdp_glbl import AddrMap

from ucdp_ipxact import get_parser


@click.group()
def ipxact():
    """IPXACT Commands."""


@ipxact.command()
@click.argument("ipxact", type=click.Path(exists=True))
def check(ipxact: Path):
    """Check - Validate IPXACT and try to import."""
    ipxact = Path(ipxact)
    parser = get_parser(ipxact)
    parser.is_compatible(ipxact)
    print(f"valid: {parser.validate(ipxact)}")
    # parser.parse(ipxact)
    print(f"{str(ipxact)!r} checked.")

    comp = parser._read(ipxact)

    addrspace = tuple(parser._get_addrspaces(comp))
    print(repr(addrspace[0]))
    for word in addrspace[0].words:
        print(word)
        for field in word.fields:
            print(field)
            # field_type = field.type_
            # if field_type is not u.UintType(field_type.width):
            #     for item in field_type.values():
            #         print("  ", item)
    addrmap = AddrMap.from_addrspaces(list(addrspace))
    print(addrmap.get_overview())
