from dataclasses import dataclass
from typing import List

@dataclass
class User:
    id: int
    name: str
    email: str
    password: str