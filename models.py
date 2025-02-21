from dataclasses import dataclass
from typing import Optional


@dataclass
class ScrapingResult:
    raw_content: str
    cleaned_content: str
    success: bool
    error: Optional[str] = None
