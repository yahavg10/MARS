from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Components:
    database: Dict[str, Any]
    sender: Dict[str, Any]
    pipeline_executor: Dict[str, Any]
