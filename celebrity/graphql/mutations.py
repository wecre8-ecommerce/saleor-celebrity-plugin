import mimetypes
import os.path
import secrets
import urllib.request

import graphene
import phonenumbers
import requests
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.validators import validate_email
from phonenumber_field.phonenumber import PhoneNumber

from saleor.graphql.account.enums import CountryCodeEnum
from saleor.graphql.core.mutations import ModelDeleteMutation, ModelMutation
from saleor.graphql.core.types import Upload
from saleor.product.models import Product
from celebrity import models
from celebrity.graphql import enums, types
from celebrity.graphql.errors import CelebrityError


def get_filename_from_url(url: str):
    """Prepare unique filename for file from URL to avoid overwriting."""
    file_name = os.path.basename(url)
    name, format = os.path.splitext(file_name)
    hash = secrets.token_hex(nbytes=4)
    return f"{name}_{hash}{format}"


def is_image_url(url: str):
    """Check if file URL seems to be an image."""
    req = urllib.request.Request(
        url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"}
    )
    r = urllib.request.urlopen(req)
    if "image" in r.getheader("Content-Type"):
        return True
    filetype = mimetypes.guess_type(url)[0]
    return filetype is not None


def upload_image(image_data, image_name):
    image_file = File(image_data.raw, image_name)
    errors = {}
    if image_file:
        return image_file
    else:
        errors["image_url"] = ValidationError(
            "Invalid  image url.",
            code=enums.VendorErrorCode.INVALID_IMAGE_URL,
        )
        raise ValidationError(errors)


class CelebrityInput(graphene.InputObjectType):
    is_active = graphene.Boolean(
        description="Active status of the Celebrity.", default_value=True
    )
    phone_number = graphene.String(description="Phone number.")
    email = graphene.String(description="Phone number.")
    country = CountryCodeEnum(description="Country code.")
    city = graphene.String(description="City of the Celebrity.")
    website_url = graphene.String(description="Website of the Celebrity.")
    instagram_url = graphene.String(description="Instagram Link of the Celebrity.")
    twitter_url = graphene.String(description="Twitter Link of the Celebrity.")
    bio = graphene.String(description="Bio of the Celebrity.")
    about = graphene.String(description="about of the Celebrity.")

    variants = graphene.List(
        graphene.ID,
        description="Product Variant IDs to add to the celebrity.",
    )

    logo = Upload(description="Celebrity logo")
    header_image = Upload(required=False, description="Header image.")


class CelebrityCreateInput(CelebrityInput):
    first_name = graphene.String(
        description="The first name of the Celebrity.", required=True
    )
    last_name = graphene.String(
        description="The last name of the Celebrity.", required=True
    )
    phone_number = graphene.String(description="Phone number.", required=True)
    email = graphene.String(description="Phone number.", required=True)


class CelebrityCreate(ModelMutation):
    class Arguments:
        input = CelebrityCreateInput(
            required=True, description="Fields required to create a Celebrity."
        )

    class Meta:
        description = "Create a new Celebrity."
        model = models.Celebrity
        error_type_class = CelebrityError
        object_type = types.Celebrity
        # permissions = (CelebrityPermissions.MANAGE_CELEBRITY,)

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        errors = {}

        if len(data["first_name"]) == 0:
            errors["first_name"] = ValidationError(
                "Invalid first name.",
                code=enums.CelebrityErrorCode.INVALID_FIRST_NAME,
            )

        if len(data["last_name"]) == 0:
            errors["last_name"] = (
                ValidationError(
                    message="Invalid last name.",
                    code=enums.CelebrityErrorCode.INVALID_LAST_NAME,
                ),
            )

        if email := data.get("email"):
            try:
                validate_email(email)
            except ValidationError:
                errors["email"] = ValidationError(
                    "Provided email is invalid.",
                    code=enums.CelebrityErrorCode.INVALID_EMAIL,
                )

        try:
            phone_number = data["phone_number"]
            PhoneNumber.from_string(phone_number).is_valid()
        except phonenumbers.phonenumberutil.NumberParseException as e:
            errors["phone_number"] = ValidationError(
                str(e), code=enums.CelebrityErrorCode.INVALID_PHONE_NUMBER
            )

        if errors:
            raise ValidationError(errors)

        return cleaned_input


class CelebrityUpdateInput(CelebrityInput):
    first_name = graphene.String(description="The first name of the Celebrity.")
    last_name = graphene.String(description="The last name of the Celebrity.")


class CelebrityUpdate(ModelMutation):
    class Arguments:
        id = graphene.ID(required=True, description="Celebrity ID.")
        input = CelebrityUpdateInput(
            description="Fields required to update the Celebrity.", required=True
        )

    class Meta:
        description = "Update a Celebrity."
        model = models.Celebrity
        error_type_class = CelebrityError
        object_type = types.Celebrity
        # permissions = (CelebrityPermissions.MANAGE_CELEBRITY,)


class CelebrityDelete(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(required=True, description="Celebrity ID.")

    class Meta:
        description = "Delete the Celebrity."
        model = models.Celebrity
        error_type_class = CelebrityError
        object_type = types.Celebrity
        # permissions = (CelebrityPermissions.MANAGE_CELEBRITY,)


class CelebrityUpdateLogo(ModelMutation):
    class Arguments:
        id = graphene.ID(required=True, description="celebrity ID.")
        image_url = graphene.String(required=True, description="Logo image.")

    class Meta:
        description = "Update celebrity logo image"
        model = models.Celebrity
        error_type_class = CelebrityError
        object_type = types.Celebrity

    @classmethod
    def perform_mutation(cls, _root, info, id, image_url):
        celebrity = cls.get_node_or_error(info, id, only_type="Celebrity")
        errors = {}
        if is_image_url(image_url) and celebrity:
            logo_name = get_filename_from_url(image_url)
            try:
                image_data = requests.get(image_url, stream=True)
                image_file = upload_image(image_data, logo_name)
                celebrity.logo = image_file
                celebrity.save()

            except Exception:
                errors["image_url"] = ValidationError(
                    "Invalid  image url.",
                    code=enums.CelebrityErrorCode.INVALID_IMAGE_URL,
                )

        else:
            errors["image_url"] = ValidationError(
                "Invalid  image url.",
                code=enums.CelebrityErrorCode.INVALID_IMAGE_URL,
            )

        if errors:
            raise ValidationError(errors)

        return cls(celebrity=celebrity)


class CelebrityUpdateHeader(ModelMutation):
    class Arguments:
        id = graphene.ID(required=True, description="Celebrity ID.")
        image_url = graphene.String(required=True, description="Header image.")

    class Meta:
        description = "Update Celebrity header image"
        model = models.Celebrity
        error_type_class = CelebrityError
        object_type = types.Celebrity

    @classmethod
    def perform_mutation(cls, _root, info, id, image_url):
        celebrity = cls.get_node_or_error(info, id, only_type="Celebrity")
        errors = {}
        if is_image_url(image_url) and celebrity:
            header_name = get_filename_from_url(image_url)
            try:
                image_data = requests.get(image_url, stream=True)
                image_file = upload_image(image_data, header_name)
                celebrity.header_image = image_file
                celebrity.save()

            except Exception:
                errors["image_url"] = ValidationError(
                    "Invalid  image url.",
                    code=enums.CelebrityErrorCode.INVALID_IMAGE_URL,
                )

        else:
            errors["image_url"] = ValidationError(
                "Invalid  image url.",
                code=enums.CelebrityErrorCode.INVALID_IMAGE_URL,
            )

        if errors:
            raise ValidationError(errors)

        return cls(celebrity=celebrity)


class CelebrityAddProducts(ModelMutation):
    class Arguments:
        id = graphene.ID(required=True, description="Celebrity ID.")
        products = graphene.List(
            graphene.ID,
            description="product IDs to Assign to the celebrity",
        )

    class Meta:
        description = "Add a product to Celebrity "
        model = models.Celebrity
        error_type_class = CelebrityError
        object_type = types.Celebrity

    @classmethod
    def perform_mutation(cls, _root, info, id, products):
        celebrity = cls.get_node_or_error(info, id, only_type="Celebrity")
        product_ids = cls.get_global_ids_or_error(
            products, only_type="Product", field="products"
        )
        celebrity.products.add(*product_ids)
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            info.context.plugins.product_updated(product)
        return cls(celebrity=celebrity)


class CelebrityRemoveProducts(ModelMutation):
    class Arguments:
        id = graphene.ID(required=True, description="Celebrity ID.")
        products = graphene.List(
            graphene.ID,
            description="product IDs to Remove from the celebrity",
        )

    class Meta:
        description = "Add a product to Celebrity "
        model = models.Celebrity
        error_type_class = CelebrityError
        object_type = types.Celebrity

    @classmethod
    def perform_mutation(cls, _root, info, id, products):
        celebrity = cls.get_node_or_error(info, id, only_type="Celebrity")
        product_ids = cls.get_global_ids_or_error(
            products, only_type="Product", field="products"
        )
        celebrity.products.remove(*product_ids)
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            info.context.plugins.product_updated(product)
        return cls(celebrity=celebrity)
