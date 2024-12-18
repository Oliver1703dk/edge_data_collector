from PIL import Image
import os

def compress_image(input_path, output_path, quality=85):
    """
    Compresses an image to reduce its file size while maintaining acceptable quality.

    Args:
        input_path (str): Path to the input image file.
        output_path (str): Path to save the compressed image.
        quality (int): Quality of the output image (1-100, higher means better quality). Default is 85.

    Returns:
        str: Path to the compressed image.
    """
    try:
        # Open the image
        with Image.open(input_path) as img:
            # Ensure the image is in RGB mode (required for JPEG compression)
            if img.mode in ("RGBA", "P"):  # Convert if necessary
                img = img.convert("RGB")

            # Save the image with compression
            img.save(output_path, "JPEG", quality=quality)

        print(f"Image compressed and saved to {output_path}")
        return output_path

    except Exception as e:
        print(f"Error compressing image: {e}")
        raise
