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

import sys
from contextlib import contextmanager
from pathlib import Path

import click
import ucdp as u

from ucdp_ipxact import UcdpIpxact, get_parser

ipxact = u.cli.get_group("IPXACT Commands")


@contextmanager
def _load(console, filepath: Path) -> UcdpIpxact:
    try:
        parser = get_parser(filepath)
        parser.validate(filepath)
        ucdp_ipxact = parser.parse(filepath)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print(f"'{filepath!s}' is INVALID.")
        sys.exit(1)
    yield ucdp_ipxact


@ipxact.command()
@click.argument("ipxact", type=click.Path(exists=True, path_type=Path))
@u.cli.pass_ctx
def check(ctx, ipxact: Path):
    """Validate IPXACT and convert to UCDP Format."""
    with _load(ctx.console, ipxact):
        print(f"'{ipxact!s}' is valid.")


@ipxact.command()
@click.argument("ipxact", type=click.Path(exists=True, path_type=Path))
@u.cli.pass_ctx
def overview(ctx, ipxact: Path):
    """Load IPXACT and Show Overview."""
    with _load(ctx.console, ipxact) as ucdp_result:
        print(ucdp_result.get_overview())
