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
    extraction_id: int
    text: str
    location: str  # ej: "Página 3, párrafo 2"
    researcher_id: int
    tags: List[Tag] = field(default_factory=list)

    def add_tag(self, tag: Tag):
        if not any(t.id == tag.id for t in self.tags):
            self.tags.append(tag)

    def replace_tag(self, old_tag: Tag, new_tag: Tag):
        """
        Reemplaza una etiqueta por otra.
        Si la nueva ya existe, solo elimina la vieja.
        """
        self.tags = [t for t in self.tags if t.id != old_tag.id]

        self.add_tag(new_tag)