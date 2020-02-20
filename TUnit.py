from dataclasses import dataclass

@dataclass
class TUnit:
    sentence: str
    rank: int = None
    url: str
    categories: list
    access_timestamp: int
    latitude: float = None
    longitude: float = None
    
    has_superlative: bool
    has_contrasting: bool
    root_word: str
    subj_word: str
    readability: int