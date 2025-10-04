import os
import time
import argparse
import subprocess  # For shutdown
try:
    from picamera2 import Picamera2
    PICAMERA2_AVAILABLE = True
except ImportError:
    PICAMERA2_AVAILABLE = False
try:
    from picamera import PiCamera
except ImportError:
    from edge_data_collector.camera.mock.pi_camera import PiCamera  # Adjust import if using your mock

def record_video(output_folder=None, duration=30, resolution=(1920, 1080), fps=30):
    """
    Record a video clip using Picamera2 or legacy PiCamera.
    
    Args:
        output_folder (str): Folder to save videos (default: 'videos' relative to script dir).
        duration (int): Recording length in seconds (default: 30).
        resolution (tuple): Video resolution (width, height) (default: (1920, 1080)).
        fps (int): Frames per second (default: 30).
    
    Returns:
        str: Path to the saved video file, or None if failed.
    """
    # Default to 'videos' folder in script's directory
    if output_folder is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_folder = os.path.join(script_dir, "videos")
    
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Generate timestamp for filename
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    video_filename = f"flood_video_{timestamp}.h264"
    video_path = os.path.join(output_folder, video_filename)
    
    camera = None
    try:
        print(f"Starting {duration}s video recording to {video_path}...")
        
        if PICAMERA2_AVAILABLE:
            # Use Picamera2 (modern, recommended)
            camera = Picamera2()
            config = camera.create_video_configuration(main={"size": resolution, "format": "XRGB8888"})
            camera.configure(config)
            camera.framerate = fps
            camera.start_recording(controls={"FrameDurationLimits": (33333, 33333)}, filename=video_path)  # ~30fps
        else:
            # Fallback to legacy PiCamera
            camera = PiCamera()
            camera.resolution = resolution
            camera.framerate = fps
            camera.start_recording(video_path)
        
        # Record for specified duration
        time.sleep(duration)
        
        # Stop recording
        if PICAMERA2_AVAILABLE:
            camera.stop_recording()
        else:
            camera.stop_recording()
        
        print(f"Video saved successfully: {video_path}")
        return video_path
        
        # Automatic shutdown after successful recording
        subprocess.call(['sudo', 'shutdown', '-h', 'now'])
        print("Shutdown initiated.")  # Won't reach here in practice
        
    except Exception as e:
        print(f"Failed to record video: {e}")
        return None
    finally:
        # Clean shutdown
        if camera:
            if PICAMERA2_AVAILABLE:
                camera.stop()
                camera.close()
            else:
                camera.close()
            print("Camera closed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Record a short video clip from Raspberry Pi camera.")
    parser.add_argument("--folder", type=str, default=None, help="Output folder for videos (default: 'videos' in script dir)")
    parser.add_argument("--duration", type=int, default=30, help="Recording duration in seconds (default: 30)")
    parser.add_argument("--resolution", type=str, default="1920,1080", help="Resolution as 'width,height' (default: 1920,1080)")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second (default: 30)")
    
    args = parser.parse_args()
    
    # Parse resolution
    res = tuple(map(int, args.resolution.split(',')))
    
    record_video(
        output_folder=args.folder,
        duration=args.duration,
        resolution=res,
        fps=args.fps
    )