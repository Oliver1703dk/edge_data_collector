import os
import time

class PiCamera:
    def __init__(self):
        print("Mock PiCamera initialized")
        self.resolution = (1920, 1080)  # Default resolution
        self.is_open = True

    def capture(self, output_path):
        if not self.is_open:
            raise RuntimeError("Mock PiCamera is closed and cannot capture images.")
        
        print(f"Mock capture started with resolution: {self.resolution}")
        
        # Simulate image creation by writing dummy data to the file
        try:
            with open(output_path, "wb") as f:
                f.write(os.urandom(1024 * 1024))  # Create a 1MB dummy file
            print(f"Mock capture saved to {output_path}")
        except Exception as e:
            print(f"Failed to save mock capture: {e}")
            raise

    def close(self):
        if self.is_open:
            print("Mock PiCamera closed")
            self.is_open = False
        else:
            print("Mock PiCamera is already closed")

    def set_resolution(self, width, height):
        """Set the resolution of the mock camera."""
        if not self.is_open:
            raise RuntimeError("Cannot set resolution on a closed Mock PiCamera.")
        self.resolution = (width, height)
        print(f"Mock PiCamera resolution set to: {self.resolution}")

    # Compatibility with Picamera2 API
    def capture_file(self, output_path):
        """Capture an image to a file (Picamera2-compatible)."""
        self.capture(output_path)
