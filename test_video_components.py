"""
Test script for main_video.py components

This script tests the VideoHandler and StaticSensorHandler classes
without requiring a full video file. It creates a simple test video
and verifies the functionality.
"""

import cv2
import numpy as np
import os
import sys
import tempfile

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main_video import VideoHandler, StaticSensorHandler


def create_test_video(output_path, duration_seconds=5, fps=30):
    """
    Create a simple test video with colored frames and frame numbers.
    
    Args:
        output_path (str): Path where to save the test video
        duration_seconds (int): Duration of the video in seconds
        fps (int): Frames per second
    
    Returns:
        str: Path to the created video file
    """
    print(f"Creating test video: {output_path}")
    
    # Video properties
    width, height = 640, 480
    total_frames = duration_seconds * fps
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    if not out.isOpened():
        raise RuntimeError("Failed to create video writer")
    
    # Generate frames
    for frame_num in range(total_frames):
        # Create a frame with changing colors
        hue = int((frame_num / total_frames) * 180)
        frame = np.ones((height, width, 3), dtype=np.uint8)
        frame[:, :] = cv2.cvtColor(
            np.array([[[hue, 255, 255]]], dtype=np.uint8),
            cv2.COLOR_HSV2BGR
        )[0, 0]
        
        # Add frame number text
        text = f"Frame {frame_num + 1}/{total_frames}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, text, (50, height // 2), font, 1, (255, 255, 255), 2)
        
        # Write frame
        out.write(frame)
    
    out.release()
    print(f"Test video created: {total_frames} frames at {fps} fps")
    return output_path


def test_video_handler():
    """Test the VideoHandler class."""
    print("\n" + "="*60)
    print("Testing VideoHandler")
    print("="*60)
    
    # Create a temporary test video
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp_file:
        test_video_path = tmp_file.name
    
    try:
        # Create test video
        create_test_video(test_video_path, duration_seconds=3, fps=10)
        
        # Initialize VideoHandler
        print("\nInitializing VideoHandler...")
        video_handler = VideoHandler(
            video_path=test_video_path,
            camera_id="test_camera"
        )
        
        # Test frame extraction
        print("\nExtracting frames...")
        frame_count = 0
        max_frames = 5  # Only extract first 5 frames for testing
        
        while video_handler.has_frames() and frame_count < max_frames:
            frame_path, capture_ts = video_handler.capture_frame()
            if frame_path:
                frame_count += 1
                print(f"  ✓ Frame {frame_count} extracted: {os.path.basename(frame_path)}")
                # Verify the file exists and has content
                if os.path.exists(frame_path) and os.path.getsize(frame_path) > 0:
                    print(f"    File size: {os.path.getsize(frame_path)} bytes")
                    print(f"    Capture timestamp: {capture_ts}")
                else:
                    print(f"    ✗ Error: Frame file is invalid")
            else:
                break
        
        # Test video properties
        print(f"\nVideo properties:")
        print(f"  FPS: {video_handler.fps}")
        print(f"  Total frames: {video_handler.total_frames}")
        print(f"  Current frame: {video_handler.current_frame}")

        # Test aligned capture at specific timestamp
        target_time = 1.0  # seconds
        sequence_number = 42
        aligned_frame, capture_ts = video_handler.capture_frame_at(
            time_seconds=target_time,
            sequence_number=sequence_number
        )
        if aligned_frame:
            print(f"\n✓ Aligned frame extracted at {target_time}s: {os.path.basename(aligned_frame)}")
            print(f"  Capture timestamp: {capture_ts}")
        else:
            print(f"\n✗ Failed to extract aligned frame at {target_time}s")
        
        # Clean up
        video_handler.close()
        print("\n✓ VideoHandler test completed successfully!")
        
    except Exception as e:
        print(f"\n✗ VideoHandler test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up test video
        if os.path.exists(test_video_path):
            os.remove(test_video_path)
            print(f"Cleaned up test video: {test_video_path}")


def test_static_sensor_handler():
    """Test the StaticSensorHandler class."""
    print("\n" + "="*60)
    print("Testing StaticSensorHandler")
    print("="*60)
    
    try:
        # Test with default values
        print("\nTest 1: Default values")
        sensor_handler = StaticSensorHandler()
        data = sensor_handler.read_sensor_data()
        print(f"  Temperature: {data['temperature']}°C")
        print(f"  Humidity: {data['humidity']}%")
        print(f"  Pressure: {data['pressure']} hPa")
        
        # Verify data structure
        assert 'temperature' in data, "Missing temperature"
        assert 'humidity' in data, "Missing humidity"
        assert 'pressure' in data, "Missing pressure"
        print("  ✓ Data structure is correct")
        
        # Test with custom values
        print("\nTest 2: Custom values")
        sensor_handler = StaticSensorHandler(
            temperature=25.5,
            humidity=60.0,
            pressure=1015.0
        )
        data = sensor_handler.read_sensor_data()
        print(f"  Temperature: {data['temperature']}°C")
        print(f"  Humidity: {data['humidity']}%")
        print(f"  Pressure: {data['pressure']} hPa")
        
        # Verify custom values
        assert data['temperature'] == 25.5, "Temperature mismatch"
        assert data['humidity'] == 60.0, "Humidity mismatch"
        assert data['pressure'] == 1015.0, "Pressure mismatch"
        print("  ✓ Custom values are correct")
        
        # Test multiple reads return same data
        print("\nTest 3: Consistency check")
        data1 = sensor_handler.read_sensor_data()
        data2 = sensor_handler.read_sensor_data()
        assert data1 == data2, "Data should be consistent"
        print("  ✓ Data is consistent across multiple reads")
        
        print("\n✓ StaticSensorHandler test completed successfully!")
        
    except Exception as e:
        print(f"\n✗ StaticSensorHandler test failed: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("MAIN_VIDEO.PY COMPONENT TESTS")
    print("="*60)
    
    # Check if OpenCV is available
    try:
        import cv2
        print(f"✓ OpenCV version: {cv2.__version__}")
    except ImportError:
        print("✗ OpenCV not found. Please install: pip install opencv-python")
        return
    
    # Run tests
    test_static_sensor_handler()
    test_video_handler()
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print("="*60)
    print("\nNext steps:")
    print("1. Update VIDEO_PATH in main_video.py")
    print("2. Run: python main_video.py")


if __name__ == "__main__":
    main()
