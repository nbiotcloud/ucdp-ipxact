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

"""IPXACT Version Manager."""

import importlib
import logging
from importlib.metadata import entry_points
from pathlib import Path

import ucdp as u

from .ipxact import UcdpIpxact
from .parser import Parser

LOGGER = logging.getLogger(__name__)


class ParserManager(u.Object):
    """Parser Manager collects all available IPXACT Parser."""

    _parsers: list[Parser] = u.PrivateField(default_factory=list)

    @staticmethod
    def create() -> "ParserManager":
        """Create ParserManager with all IPXACT-Parser."""
        parsermanager = ParserManager()
        for entry_point in entry_points(group="ucdp_ipxact.parser"):
            parsercls = _load(entry_point.value)
            if not issubclass(parsercls, Parser):  # pragma: no cover
                LOGGER.warning("Entrypoint %s %s is not a IPXACT-Parser", entry_point.name, entry_point.value)
                continue
            parsermanager.add(parsercls())
        return parsermanager

    def add(self, parser: Parser) -> None:
        """Add Parsers to ParserManager."""
        self._parsers.append(parser)

    @property
    def parsers(self) -> tuple[Parser, ...]:
        """Parsers."""
        return tuple(self._parsers)

    def is_compatible(self, filepath: Path) -> bool:
        """Check if Parsable."""
        filepath = u.improved_resolve(filepath, strict=True, replace_envvars=True)
        for parser in self._parsers:
            if parser.is_compatible(filepath):
                return True
        return False

    def validate(self, filepath: Path) -> bool:
        """Validate."""
        filepath = u.improved_resolve(filepath, strict=True, replace_envvars=True)
        return self.get_parser(filepath).validate(filepath)

    def parse(self, filepath: Path) -> UcdpIpxact:
        """Parse."""
        filepath = u.improved_resolve(filepath, strict=True, replace_envvars=True)
        return self.get_parser(filepath).parse(filepath)

    def get_parser(self, filepath: Path) -> Parser:
        """Returns first campatible Parser."""
        for parser in sorted(self._parsers, key=lambda parser: parser.prio, reverse=True):
            if parser.is_compatible(filepath):
                return parser
        raise ValueError(f"Unknown schema in {filepath}")


def _load(ref):
    modname, cmd_object_name = ref.rsplit(".", 1)
    mod = importlib.import_module(modname)
    return getattr(mod, cmd_object_name)


def validate(filepath: Path) -> bool:
    """Validate IPXACT."""
    parsermanager = ParserManager.create()
    return parsermanager.validate(filepath)


def parse(filepath: Path) -> UcdpIpxact:
    """Parse IPXACT."""
    parsermanager = ParserManager.create()
    return parsermanager.parse(filepath)


def get_parser(filepath: Path) -> Parser:
    """Determine Parser for IPXACT."""
    parsermanager = ParserManager.create()
    return parsermanager.get_parser(filepath)
