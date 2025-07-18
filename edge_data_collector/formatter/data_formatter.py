



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
    encoded_image_data = encode_image(image_data)
    return {
        "image_data": encoded_image_data,
        "sensor_data": sensor_data,
        "metadata": metadata
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
    


