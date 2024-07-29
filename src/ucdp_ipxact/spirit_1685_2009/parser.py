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

from collections.abc import Iterator
from functools import lru_cache
from pathlib import Path

import ucdp as u
import xmlschema
from defusedxml import ElementTree
from ucdp.docutil import doc_from_type
from ucdp.humannum import Hex
from ucdp.orientation import IN, INOUT, OUT
from ucdp.signal import Port
from ucdp.typescalar import BitType, UintType
from ucdp_addr.addrspace import Addrspace
from ucdp_ipxact import Parser

# generated with: xsdata spirit_1685_2009/xml_schema/component.xsd -ss single-package -p schema_dataclass_pkg
from ucdp_ipxact.spirit_1685_2009.xml_schema_pkg import Component
from xsdata.formats.dataclass.parsers import XmlParser

DIRECTION_MAP = {
    "in": IN,
    "out": OUT,
    "inout": INOUT,
}

ACCESS_MAP = {
    "read-only": "RO",
    "write-only": "WO",
    "read-write": "RW",
    "writeOnce": "WO",
    "read-writeOnce": "RW",
}


class GenericIpxactEnumType(u.AEnumType):
    """Generic Enum Type for Ipxact Enumerated Values."""

    keytype: u.UintType = u.UintType(8)
    iter_enumerated_values: tuple[tuple[int, str, str], ...] = u.Field(repr=False)

    def _build(self) -> None:
        for (
            idx,
            name,
            title,
        ) in self.iter_enumerated_values:
            self._add(idx, name, title=title)


@lru_cache
def _is_compatible(filepath: Path) -> bool:
    try:
        etree = ElementTree.parse(filepath)
    except Exception:
        return False
    root = etree.getroot().tag
    return "XMLSchema/SPIRIT/1685-2009}" in root


class Spirit2009Parser(Parser):
    """General IPXACT Parser."""

    @staticmethod
    def is_compatible(filepath: Path) -> bool:
        """Check if Parsable."""
        return _is_compatible(filepath)

    @staticmethod
    def validate(filepath: Path) -> bool:
        """Validate."""
        # local copy of schema: xsdata download http://www.spiritconsortium.org/XMLSchema/SPIRIT/1685-2009/index.xsd
        ipxact_schema = xmlschema.XMLSchema(Path(__file__).parent / "xml_schema" / "index.xsd")
        return ipxact_schema.is_valid(filepath)

    def _read(self, filepath: Path):
        """Map xml on Component Dataclass."""
        xml_parser = XmlParser()
        return xml_parser.parse(filepath, Component)

    def _get_vendor(self, data) -> str:
        return data.vendor

    def _get_name(self, data) -> str:
        return data.name

    def _get_library(self, data) -> str:
        return data.library

    def _get_version(self, data) -> str:
        return data.version

    def _get_ports(self, data) -> Iterator[u.Port]:
        for businterface in self._iter_bus_interfaces(data):
            for port_map in self._iter_port_maps(businterface):
                pys_port = self._find_phys_port(data, port_map.physical_port.name)
                port_direction = DIRECTION_MAP[pys_port.wire.direction.value]
                port_type = self._get_port_type(pys_port.wire.vector)
                port_comment = self._get_log_port_name(port_map)
                port_descr = None
                if pys_port.description:
                    port_descr = pys_port.description.value
                port_doc = doc_from_type(port_type, comment=port_comment, descr=port_descr)
                yield Port(port_type, pys_port.name, direction=port_direction, doc=port_doc)

    def _iter_bus_interfaces(self, comp):
        yield from comp.bus_interfaces.bus_interface

    def _iter_port_maps(self, bus_interface):
        yield from bus_interface.port_maps.port_map

    def _find_phys_port(self, comp, phys_port_name):
        for port in comp.model.ports.port:
            if port.name == phys_port_name:
                return port
        raise ValueError(f"No Physical Port {phys_port_name} found.")

    def _get_port_type(self, port_vector):
        port_type = BitType()
        if port_vector:
            left = int(port_vector.left.value)
            right = int(port_vector.right.value)
            port_type = UintType(width=left - right + 1, right=right)
        return port_type

    def _get_log_port_name(self, port_map) -> str:
        name = port_map.logical_port.name
        vector = port_map.logical_port.vector
        if vector:
            left = int(vector.left.value)
            right = int(vector.right.value)
            name = name + f"[{left}:{right}]"
        return name

    def _get_addrspaces(self, data) -> Iterator[Addrspace]:
        for memory_map in self._iter_memory_maps(data):
            for addr_block in self._iter_addr_blocks(memory_map):
                addrspace = self._get_addrspace(addr_block)
                for register in self._iter_registers(addr_block):
                    word = self._add_word(addrspace, register)
                    word_default = self._get_word_default(register)
                    for field in self._iter_fields(register):
                        self._add_field(word, field, word_default)
                yield addrspace

    def _get_word_default(self, register):
        mask = register.reset.mask
        word_default = Hex(register.reset.value.value)
        if mask:
            word_default = word_default & Hex(mask.value)
        return word_default

    def _get_field_default(self, field, word_default):
        slice_right = field.bit_offset
        slice_left = slice_right + field.bit_width.value - 1
        slice = u.slices.Slice(left=slice_left, right=slice_right)
        return slice.extract(word_default)

    def _add_field(self, word, field, word_default):
        word.add_field(
            field.name.lower(),
            self._get_field_type(field, self._get_field_default(field, word_default)),
            ACCESS_MAP[field.access.value.value],
            offset=field.bit_offset,
            descr=field.description.value,
            is_volatile=self._get_volatile(field),
        )

    def _iter_fields(self, register):
        yield from register.field_value

    def _add_word(self, addrspace, register):
        return addrspace.add_word(
            name=register.name.lower(),
            offset=Hex(register.address_offset),
            descr=register.description.value,
            title=register.display_name.value,
            is_volatile=self._get_volatile(register),
        )

    def _get_field_enum_type(self, field):
        for val in field.enumerated_values.enumerated_value:
            yield (Hex(val.value), val.name, val.display_name.value)

    def _get_field_type(self, field, default):
        field_type = u.UintType(field.bit_width.value, default=default)
        if field.enumerated_values:
            field_type = GenericIpxactEnumType(
                keytype=UintType(field.bit_width.value, default=default),
                iter_enumerated_values=tuple(self._get_field_enum_type(field)),
            )
        return field_type

    def _get_volatile(self, cls) -> bool:
        volatile = False
        if cls.volatile:
            volatile = cls.volatile.value
        return volatile

    def _iter_registers(self, addr_block):
        yield from addr_block.register

    def _get_addrspace(self, addr_block) -> Addrspace:
        addrspace_name = addr_block.name
        addrspace_baseaddr = Hex(addr_block.base_address.value)
        addrspace_size = Hex(addr_block.range.value)
        addrspace_width = addr_block.width.value
        return Addrspace(
            name=addrspace_name,
            baseaddr=addrspace_baseaddr,
            width=addrspace_width,
            size=addrspace_size,
        )

    def _iter_memory_maps(self, comp):
        yield from comp.memory_maps.memory_map

    def _iter_addr_blocks(self, memory_map):
        yield from memory_map.address_block
