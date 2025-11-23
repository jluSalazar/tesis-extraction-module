from dataclasses import dataclass, field
from typing import List, Optional
from .tag import Tag

@dataclass
class Quote:
    """
    Entidad secundaria.
    Representa un fragmento extraído. Su ciclo de vida depende de Extraction.
    """
    id: Optional[int]
    extraction_id: Optional[int]
    text: str
    location: str  # ej: "Página 3, párrafo 2"
    researcher_id: int
    tags: List[Tag] = field(default_factory=list)

    def add_tag(self, tag: Tag):
        # Lógica de negocio simple: no permitir duplicados
        if tag not in self.tags:
            self.tags.append(tag)