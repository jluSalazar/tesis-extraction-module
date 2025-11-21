def list_available_tags_for_user(self, user_id: int, project_id: int) -> List[Tag]:
    from django.db.models import Q

    # Regla de visibilidad:
    # 1. Tags del proyecto
    # 2. Y (son Públicos O fueron creados por MÍ)
    qs = TagModel.objects.filter(
        project_id=project_id
    ).filter(
        Q(visibility='Public') | Q(created_by_id=user_id)
    )

    return [TagMapper.to_domain(m) for m in qs]