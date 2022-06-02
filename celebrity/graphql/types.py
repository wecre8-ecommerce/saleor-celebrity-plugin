import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from saleor.graphql.account.enums import CountryCodeEnum
from saleor.graphql.core.types.common import Image
from saleor.graphql.core.connection import CountableConnection

from celebrity import models


class CountableDjangoObjectType(DjangoObjectType):
    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, *args, **kwargs):
        # Force it to use the countable connection
        countable_conn = CountableConnection.create_type(
            "{}CountableConnection".format(cls.__name__), node=cls
        )
        super().__init_subclass_with_meta__(*args, connection=countable_conn, **kwargs)



class Celebrity(CountableDjangoObjectType):
    products = graphene.List(graphene.ID, description="List of products IDs.")
    product_slugs = graphene.List(
        graphene.String, description="List of products slugs."
    )
    logo = graphene.Field(Image, size=graphene.Int(description="Size of the image."))
    header_image = graphene.Field(
        Image, size=graphene.Int(description="Size of the image.")
    )
    country = CountryCodeEnum(description="Country.")

    class Meta:
        model = models.Celebrity
        filter_field = ["id", "first_name", "phone_number", "email"]
        interfaces = (graphene.relay.Node,)

    def resolve_products(root, info):
        return [
            graphene.Node.to_global_id("Product", id)
            for id in root.products.values_list("id", flat=True)
        ]

    def resolve_product_slugs(root, info):
        return [(slug) for slug in root.products.values_list("slug", flat=True)]

    def resolve_logo(root, info, size=None):
        if root.logo:
            return Image.get_adjusted(
                image=root.logo,
                alt=f"{root.first_name}'s logo",
                size=size,
                rendition_key_set="logo",
                info=info,
            )

    def resolve_header_image(root, info, size=None):
        if root.header_image:
            return Image.get_adjusted(
                image=root.header_image,
                alt=f"{root.first_name}'s header image",
                size=size,
                rendition_key_set="background_images",
                info=info,
            )


class CelebrityConnection(relay.Connection):
    class Meta:
        node = Celebrity
