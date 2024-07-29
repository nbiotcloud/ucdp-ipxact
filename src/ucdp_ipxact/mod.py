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

"""Unified Chip Design Platform - IPXACT."""

from collections.abc import Iterator
from functools import cached_property, lru_cache
from inspect import getfile
from logging import getLogger
from pathlib import Path

import ucdp as u
from ucdp_addr import Addrspace

from .ipxact import UcdpIpxact
from .parsermanager import ParserManager

LOGGER = getLogger(__name__)


@lru_cache
def _get_parsermanager() -> ParserManager:
    return ParserManager.create()


@lru_cache
def _parse(filepath: Path) -> UcdpIpxact:
    """Parse IPXACT."""
    LOGGER.info("Reading %s", filepath)
    return _get_parsermanager().parse(filepath)


def _load(mod: u.BaseMod, filepath: Path) -> UcdpIpxact:
    basedir = Path(getfile(mod.parent.__class__)).parent if mod.parent else None
    filepath = u.improved_resolve(filepath, basedir=basedir, strict=True, replace_envvars=True)
    return _parse(filepath)


class UcdpIpxactMod(u.ATailoredMod):
    """IPXACT Import Module."""

    filepath: Path

    @cached_property
    def ipxact(self) -> UcdpIpxact:
        """IPXACT."""
        return _load(self, self.filepath)

    def _build(self):
        ipxact = self.ipxact
        for port in ipxact.ports:
            name = port.name
            self.namespace[name] = port
            self.portssignals[name] = port
            self.ports[name] = port

    @property
    def modname(self) -> str:
        """Module Name."""
        return self.ipxact.name

    @property
    def libname(self) -> str:
        """Library Name."""
        return self.ipxact.libname

    def get_addrspaces(self) -> Iterator[Addrspace]:
        """Address Spaces."""
        yield from self.ipxact.addrspaces

    def get_overview(self) -> str:
        """Overview."""
        return self.ipxact.get_overview()
