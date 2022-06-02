import graphene

from saleor.graphql.core.types.common import Error
from celebrity.graphql import enums

CelebrityErrorCode = graphene.Enum.from_enum(enums.CelebrityErrorCode)


class CelebrityError(Error):
    code = CelebrityErrorCode(description="The error code.", required=True)
