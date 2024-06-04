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

"""Unified Chip Design Platform - IPXACT Validator."""

from pathlib import Path

import ucdp as u
from lxml import etree
from ucdp.nameutil import didyoumean

VALID_IPXACT_SCHEMA = [
                        # "XMLSchema/IPXACT/1685-2022-VE-1.0",
                        "XMLSchema/IPXACT/1685-2022",
                        "XMLSchema/IPXACT/1685-2014",
                        "XMLSchema/SPIRIT/1685-2009-VE-1.0",
                        "XMLSchema/SPIRIT/1685-2009",
                       ]

def extract_root_schema(lxml_etree: etree) -> tuple[str, str]:
    """Extract XML root name and local schema path."""
    root = lxml_etree.getroot().tag
    pos = root.find("}")
    root_name = root[pos+1:]
    schema_path = root[root.find("XMLSchema/"):pos]
    return (root_name, schema_path)

def check_valid_ipxact_schema(schema_path: str) -> Path:
    """Check for valid IPXACT schema paths."""
    if schema_path not in VALID_IPXACT_SCHEMA:
        dym = didyoumean(schema_path, VALID_IPXACT_SCHEMA, known=True)
        raise ValueError(f"Found Schema '{schema_path}' not supported: {dym}") from None
    THIS_DIR = Path(__file__).parent
    xsd_path = THIS_DIR / schema_path / "index.xsd"
    return xsd_path

def validate(path: Path):
    """Validate IPXACT at `path`."""
    xml_path = u.improved_resolve(path, strict=True, replace_envvars=True)
    # your validate goes here
    if not xml_path.exists():
        raise ValueError("Invalid")

    xml_doc = etree.parse(xml_path)
    root_name, schema_path = extract_root_schema(xml_doc)
    xsd_path = check_valid_ipxact_schema(schema_path)
    xmlschema_doc = etree.parse(xsd_path)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    result = xmlschema.validate(xml_doc)
    if not result:
        raise ValueError(f"XML file. Is not matching with schema.")
