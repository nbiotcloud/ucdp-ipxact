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

"""IPXACT Parser."""

from abc import abstractmethod
from collections.abc import Iterator
from pathlib import Path

import ucdp as u
from ucdp_addr.addrspace import Addrspace

from .ipxact import UcdpIpxact


class Parser(u.Object):
    """General IPXACT Parser."""

    prio: int = 0

    @staticmethod
    def is_compatible(filepath: Path) -> bool:
        """Check if Parsable."""
        raise NotImplementedError

    @staticmethod
    def validate(filepath: Path) -> bool:
        """Validate."""
        raise NotImplementedError

    def parse(self, filepath: Path) -> UcdpIpxact:
        """Parse."""
        data = self._read(filepath)
        return UcdpIpxact(
            vendor=self._get_vendor(data),
            version=self._get_version(data),
            libname=self._get_library(data),
            name=self._get_name(data),
            ports=tuple(self._get_ports(data)),
            addrspaces=tuple(self._get_addrspaces(data)),
        )

    @abstractmethod
    def _read(self, filepath: Path):
        raise NotImplementedError

    @abstractmethod
    def _get_vendor(self, data) -> str:
        raise NotImplementedError

    @abstractmethod
    def _get_name(self, data) -> str:
        raise NotImplementedError

    @abstractmethod
    def _get_library(self, data) -> str:
        raise NotImplementedError

    @abstractmethod
    def _get_version(self, data) -> str:
        raise NotImplementedError

    @abstractmethod
    def _get_ports(self, data) -> Iterator[u.Port]:
        raise NotImplementedError

    @abstractmethod
    def _get_addrspaces(self, data) -> Iterator[Addrspace]:
        raise NotImplementedError
