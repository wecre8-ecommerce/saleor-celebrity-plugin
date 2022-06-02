import graphene
from graphene_federation import build_schema

from saleor.graphql.core.connection import (
    create_connection_slice,
    filter_connection_queryset,
)
from saleor.graphql.core.fields import FilterConnectionField
from saleor.graphql.core.utils import from_global_id_or_error

from celebrity import models
from celebrity.graphql import types
from celebrity.graphql.filters import CelebrityFilterInput
from celebrity.graphql.mutations import (
    CelebrityAddProducts,
    CelebrityCreate,
    CelebrityDelete,
    CelebrityRemoveProducts,
    CelebrityUpdate,
    CelebrityUpdateHeader,
    CelebrityUpdateLogo,
)


class Query(graphene.ObjectType):
    celebrity = graphene.Field(
        types.Celebrity,
        id=graphene.Argument(graphene.ID, description="Celebrity ID", required=True),
        description="Look up a celebrity by ID",
    )
    celebrities = FilterConnectionField(
        types.CelebrityConnection,
        filter=CelebrityFilterInput(description="Filtering options for group."),
    )

    def resolve_celebrity(root, info, id, **kwargs):
        _, id = from_global_id_or_error(id, types.Celebrity)
        return models.Celebrity.objects.get(id=id)

    def resolve_celebrities(root, info, **kwargs):
        qs = models.Celebrity.objects.all()
        qs = filter_connection_queryset(qs, kwargs)
        return create_connection_slice(qs, info, kwargs, types.CelebrityConnection)


class Mutation(graphene.ObjectType):
    celebrity_create = CelebrityCreate.Field()
    celebrity_update = CelebrityUpdate.Field()
    celebrity_delete = CelebrityDelete.Field()

    celebrity_add_products = CelebrityAddProducts.Field()
    celebrity_remove_products = CelebrityRemoveProducts.Field()

    celebrity_update_logo = CelebrityUpdateLogo.Field()
    celebrity_update_header = CelebrityUpdateHeader.Field()


schema = build_schema(
    query=Query,
    mutation=Mutation,
    types=[types.Celebrity],
)
