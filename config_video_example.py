"""
Example configuration for main_video.py

Copy the relevant sections to main_video.py and adjust values as needed.
"""

# ============================================================================
# VIDEO CONFIGURATION
# ============================================================================

# Path to your video file
# Supported formats: .mp4, .avi, .mov, .mkv, and other OpenCV-supported formats
VIDEO_PATH = "path/to/your/video.mp4"

# Camera/Video source identifier
CAMERA_ID = "video_camera_01"


# ============================================================================
# STATIC SENSOR DATA CONFIGURATION
# ============================================================================

# Temperature in Celsius
STATIC_TEMPERATURE = 22.5

# Humidity percentage (0-100)
STATIC_HUMIDITY = 55.0

# Atmospheric pressure in hPa (hectopascals)
STATIC_PRESSURE = 1013.25


# ============================================================================
# FRAME PROCESSING CONFIGURATION
# ============================================================================

# Frame processing interval in seconds
# - Set to 0: Process frames as fast as possible
# - Set to 1.0: Process one frame per second
# - Set to 1/30 (0.033): Process at ~30 fps (real-time for 30fps video)
# - Set to 1/60 (0.0167): Process at ~60 fps (real-time for 60fps video)
FRAME_INTERVAL = 1.0


# ============================================================================
# EXAMPLE CONFIGURATIONS
# ============================================================================

# Example 1: Fast batch processing
# VIDEO_PATH = "/data/recordings/surveillance_2024_01_15.mp4"
# FRAME_INTERVAL = 0  # Process as fast as possible

# Example 2: Real-time simulation (30fps video)
# VIDEO_PATH = "/videos/test_footage.mp4"
# FRAME_INTERVAL = 1/30  # Match video frame rate

# Example 3: Slow sampling (one frame every 5 seconds)
# VIDEO_PATH = "/recordings/timelapse.avi"
# FRAME_INTERVAL = 5.0

# Example 4: Indoor environment monitoring
# STATIC_TEMPERATURE = 21.0  # Comfortable room temperature
# STATIC_HUMIDITY = 45.0     # Typical indoor humidity
# STATIC_PRESSURE = 1013.25  # Standard atmospheric pressure

# Example 5: Outdoor environment monitoring
# STATIC_TEMPERATURE = 15.5  # Cool outdoor temperature
# STATIC_HUMIDITY = 75.0     # Higher outdoor humidity
# STATIC_PRESSURE = 1010.0   # Slightly lower pressure
