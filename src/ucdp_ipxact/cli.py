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
from ucdp.cli import pass_ctx

from ucdp_ipxact.parser import validate
from ucdp_ipxact.ucdp_ipxact import UcdpIpxactMod


@click.group()
def ipxact():
    """IPXACT Commands."""


@ipxact.command()
@click.argument("ipxact", type=click.Path(exists=True))
@pass_ctx
def check(ctx, ipxact: Path):
    """Check - Validate IPXACT and try to import."""
    ipxact = Path(ipxact)
    validate(ipxact)
    UcdpIpxactMod(filepath=ipxact)
    ctx.console.log(f"{str(ipxact)!r} checked.")
