import os
import time  # For generating timestamps for image simulation
from .utils import compress_image
# from edge_data_collector.camera.utils import compress_image


class CameraHandler:
    def __init__(self, camera_id, image_folder="edge_data_collector/camera/images"):
        self.camera_id = camera_id
        self.image_folder = image_folder
        os.makedirs(self.image_folder, exist_ok=True)  # Ensure the image folder exists

    def capture_image(self, compress=False):
        """
        Capture an image from the camera, optionally compressing it.

        Args:
            compress (bool): Whether to compress the captured image. Default is True.

        Returns:
            str: Path to the saved image (compressed or raw).
        """
        print(f"Capturing image from camera {self.camera_id}")


        # Simulate image capture
        raw_image_path = self.simulate_image_capture()


        print(f"Raw image saved to {raw_image_path}")

        if compress:

            # Define the compressed image path
            compressed_image_path = os.path.join(self.image_folder, f"compressed_{os.path.basename(raw_image_path)}")


            # Compress the raw image
            compress_image(raw_image_path, compressed_image_path, quality=75)

            # Delete the raw image
            os.remove(raw_image_path)
            print(f"Raw image deleted: {raw_image_path}")

            return compressed_image_path
        else:
            return raw_image_path
        

    # Simulate image Capturing
    def simulate_image_capture(self):
        """
        Simulate capturing an image by creating a placeholder file.

        Returns:
            str: Path to the simulated raw image.
        """
        timestamp = int(time.time())
        raw_image_path = os.path.join(self.image_folder, f"raw_image_{timestamp}.jpg")

        # Create a placeholder raw image (for simulation purposes)
        with open(raw_image_path, "wb") as f:
            f.write(os.urandom(1024 * 1024))  # Write 1MB of random data to simulate an image

        print(f"Raw image simulated and saved to {raw_image_path}")
        return raw_image_path




# Example usage
if __name__ == "__main__":
    camera = CameraHandler(camera_id="camera_01")
    # Capture a compressed image
    compressed_image = camera.capture_image(compress=True)
    print(f"Compressed image available at: {compressed_image}")

    # Capture a raw image without compression
    raw_image = camera.capture_image(compress=False)
    print(f"Raw image available at: {raw_image}")