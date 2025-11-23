from typing import List, Optional
from ...domain.repositories.i_quote_repository import IQuoteRepository
from ...domain.entities.quote import Quote
from ..models import QuoteModel
from ..mappers.domain_mappers import QuoteMapper

class DjangoQuoteRepository(IQuoteRepository):
    def save(self, quote: Quote) -> Quote:
        # Lógica para guardar Quote y sus relaciones ManyToMany con Tags
        # Esto requiere cuidado con los IDs
        return quote # Placeholder simplificado

    def get_by_id(self, quote_id: int) -> Optional[Quote]:
        try:
            model = QuoteModel.objects.get(pk=quote_id)
            return QuoteMapper.to_domain(model)
        except QuoteModel.DoesNotExist:
            return None

    def get_by_tag(self, tag_id: int) -> List[Quote]:
        qs = QuoteModel.objects.filter(tags__id=tag_id)
        return [QuoteMapper.to_domain(m) for m in qs]

    def delete(self, quote_id: int) -> None:
        QuoteModel.objects.filter(pk=quote_id).delete()