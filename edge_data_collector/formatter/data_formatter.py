

_ALLOWED_MOTION_STATES = {"fast", "slow", "stop"}
_TRUTHY_STRINGS = {"true", "1", "yes", "on"}
_FALSY_STRINGS = {"false", "0", "no", "off"}


def _normalize_motion_hint(value):
    if isinstance(value, str):
        candidate = value.strip().lower()
        if candidate in _ALLOWED_MOTION_STATES:
            return candidate
    return "slow"


def _normalize_resource_flag(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        candidate = value.strip().lower()
        if candidate in _TRUTHY_STRINGS:
            return True
        if candidate in _FALSY_STRINGS:
            return False
        return False
    if isinstance(value, (int, float)):
        return value != 0
    return False


def format_data(image_data, sensor_data, metadata):
    """
    Formats image data, sensor data, and metadata into a JSON-like dictionary.
    Args:
        image_data (str): Path to the image file.
        sensor_data (dict): Dictionary containing sensor data.
        metadata (dict): Additional metadata for the data payload.
    Returns:
        dict: Formatted data payload with Base64-encoded image.
    """
    metadata_payload = dict(metadata or {})
    motion_hint = metadata_payload.get("motion")
    resource_flag = metadata_payload.get("resource_constrained")
    metadata_payload["motion"] = _normalize_motion_hint(motion_hint)
    metadata_payload["resource_constrained"] = _normalize_resource_flag(resource_flag)

    encoded_image_data = encode_image(image_data)
    return {
        "image_data": encoded_image_data,
        "sensor_data": sensor_data,
        "metadata": metadata_payload
    }
    

def encode_image(image_path):
    """
    Encodes an image file into Base64 format.
    Args:
        image_path (str): Path to the image file.
    Returns:
        str: Base64-encoded string of the image.
    """
    from PIL import Image
    from io import BytesIO
    import base64
    print(image_path)

    with Image.open(image_path) as img:
        buffered = BytesIO()
        img = img.convert('RGB')
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode()
    

