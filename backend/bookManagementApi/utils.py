def get_book_publish_status_by_path(path):
    status = path.split("/")[3].lower()
    assert status in ("published", "non-published")
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
