import io
from rest_framework.parsers import JSONParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


def get_book_publish_status_by_path(path):
    status = path.split("/")[3].lower()
    assert status in ("published", "non-published")
    return status


def get_book_delete_status_by_path(path):
    status = path.split("/")[3].lower()
    assert status in ("deleted", "active")
    return status


def serialize_with_custom_serializer(serializer, **serializer_fields):
    """
    Function to serialize data when there is not a model for the serializer.
    Params:
        serializer: A rest framework serializer that should have the parse_to_serialize method.
        serializer_fields: A bunch of fields that will be included to the serializer.
    Response:
        data: Data that has been serialized by the custom serializer.
    """
    assert hasattr(serializer, "parse_to_serialize")
    serialize_data = serializer.parse_to_serialize(**serializer_fields)
    serializer_instance = serializer(serialize_data)
    return serializer_instance.data


def get_json_response_from_client(raw_data):
    stream = io.BytesIO(raw_data)
    json_data = JSONParser().parse(stream)
    return json_data


def swagger_auto_schema_for_non_get_methods(serializer_class):
    def decorator(viewset_class):
        methods = ["create", "update", "partial_update", "destroy"]
        for method_name in methods:
            if hasattr(viewset_class, method_name):
                method = getattr(viewset_class, method_name)
                decorated_method = swagger_auto_schema(
                    manual_parameters=[
                        openapi.Parameter(
                            "Authorization",
                            openapi.IN_HEADER,
                            description="JWT token in 'Bearer <token>' format",
                            type=openapi.TYPE_STRING,
                            required=True,
                        )
                    ],
                    request_body=serializer_class,
                )(method)
                setattr(viewset_class, method_name, decorated_method)
        return viewset_class

    return decorator
