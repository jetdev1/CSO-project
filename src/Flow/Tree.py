import uuid
from dataclasses import dataclass, field
from typing import NamedTuple


@dataclass(frozen=True)
class Node:
    name: str
    label: str
    options: field(default_factory=list)
    
@dataclass(frozen=True)
class Option:
    label: str
    childNode: Node | str