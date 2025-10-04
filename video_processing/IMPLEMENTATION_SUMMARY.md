# main_video.py Implementation Summary

## Overview
Created a video processing mode for the Edge Data Collector system that processes pre-recorded video files instead of live camera feeds, using static sensor data instead of real sensor queries.

## Files Created/Modified

### 1. **main_video.py** (NEW)
Main script for video processing mode.

**Key Components:**
- `VideoHandler` class: Extracts frames from video files using OpenCV
  - Opens and reads video files
  - Extracts frames sequentially
  - Saves frames as JPEG images
  - Tracks video progress (current frame / total frames)
  - Provides video properties (FPS, total frames)
  
- `StaticSensorHandler` class: Provides consistent sensor readings
  - Returns static temperature, humidity, and pressure values
  - Configurable values at initialization
  - Compatible with existing data formatter

**Features:**
- Processes video frame-by-frame
- Configurable frame processing interval
- MQTT publishing support (uses existing infrastructure)
- Automatic video cleanup on completion
- Progress tracking and logging
- Compatible with existing metadata and formatting systems

**Configuration Options:**
```python
VIDEO_PATH = "path/to/your/video.mp4"  # Video file path
CAMERA_ID = "video_camera_01"          # Camera identifier
STATIC_TEMPERATURE = 22.5              # Static temperature (°C)
STATIC_HUMIDITY = 55.0                 # Static humidity (%)
STATIC_PRESSURE = 1013.25              # Static pressure (hPa)
FRAME_INTERVAL = 1.0                   # Frame processing interval (seconds)
```

### 2. **requirements.txt** (MODIFIED)
Added OpenCV dependency:
```
opencv-python==4.10.0.84
```

### 3. **README.md** (MODIFIED)
Added comprehensive documentation for video processing mode:
- Setup instructions
- Configuration guide
- Usage examples
- Feature comparison with standard mode
- Supported video formats

### 4. **config_video_example.py** (NEW)
Example configuration file with:
- Detailed parameter explanations
- Multiple usage scenarios
- Example configurations for different use cases
- Comments explaining each setting

### 5. **VIDEO_PROCESSING_GUIDE.md** (NEW)
Comprehensive quick start guide including:
- Prerequisites and installation
- Step-by-step setup instructions
- Usage examples (4 different scenarios)
- Sensor data customization examples
- Output format documentation
- Troubleshooting section
- Comparison table with main.py
- Advanced usage examples

### 6. **test_video_components.py** (NEW)
Test script for verifying functionality:
- Creates synthetic test videos
- Tests VideoHandler class
- Tests StaticSensorHandler class
- Validates frame extraction
- Checks data consistency
- Provides diagnostic output

### 7. **.gitignore** (MODIFIED)
Added patterns to exclude:
- Video files (*.mp4, *.avi, *.mov, *.mkv, etc.)
- Video directories (videos/, test_videos/)
- Maintains existing image exclusions

## Architecture

### Data Flow
```
Video File → VideoHandler → Frame (JPEG)
                                ↓
Static Values → StaticSensorHandler → Sensor Data
                                ↓
                        MetadataHandler → Metadata
                                ↓
                        DataFormatter → Formatted Data
                                ↓
                        MqttHandler → MQTT Broker (optional)
```

### Class Relationships
```
main_video.py
├── VideoHandler (replaces CameraHandler)
│   ├── cv2.VideoCapture (OpenCV)
│   └── Frame extraction & saving
├── StaticSensorHandler (replaces SensorHandler)
│   └── Static sensor data
└── Uses existing:
    ├── MetadataHandler
    ├── format_data()
    └── MqttHandler
```

## Key Differences from main.py

| Aspect | main.py | main_video.py |
|--------|---------|---------------|
| Image Source | Live camera (PiCamera) | Video file (OpenCV) |
| Sensor Data | Real sensors (Netatmo API) | Static values |
| Processing Loop | Infinite (until Ctrl+C) | Until video ends |
| Frame Rate | Camera-dependent | User-configurable |
| Hardware | Raspberry Pi + Camera | Any system with Python |
| Dependencies | picamera2/picamera | opencv-python |
| Use Case | Real-time monitoring | Batch processing, testing |

## Usage Scenarios

### 1. Development & Testing
- Test system without hardware
- Develop algorithms on recorded footage
- Validate data pipeline

### 2. Batch Processing
- Process archived surveillance footage
- Extract data from historical videos
- Analyze past events

### 3. Simulation
- Simulate real-time camera feeds
- Test MQTT infrastructure
- Demo system functionality

### 4. Training & Education
- Learn system without hardware investment
- Practice with sample videos
- Understand data flow

## Installation & Setup

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Edit main_video.py
# Update VIDEO_PATH to your video file

# Run
python main_video.py
```

### Testing
```bash
# Run component tests
python test_video_components.py
```

## Configuration Examples

### Fast Batch Processing
```python
VIDEO_PATH = "/data/archive.mp4"
FRAME_INTERVAL = 0  # Process as fast as possible
```

### Real-Time Simulation (30fps)
```python
VIDEO_PATH = "/videos/test.mp4"
FRAME_INTERVAL = 1/30  # Match video frame rate
```

### Slow Sampling
```python
VIDEO_PATH = "/recordings/timelapse.avi"
FRAME_INTERVAL = 5.0  # One frame every 5 seconds
```

## Output

### Extracted Frames
Location: `edge_data_collector/camera/images/`
Format: `video_frame_{camera_id}_{timestamp}_{frame_number}.jpg`

### Console Output
```
Video loaded: /path/to/video.mp4
FPS: 30.0, Total frames: 900
Static sensor data initialized: {'temperature': 22.5, 'humidity': 55.0, 'pressure': 1013.25}
Frame 1/900 saved to edge_data_collector/camera/images/video_frame_video_camera_01_1704123456_1.jpg
Data Published
```

## Supported Video Formats
- MP4 (`.mp4`) - Recommended
- AVI (`.avi`)
- MOV (`.mov`)
- MKV (`.mkv`)
- FLV (`.flv`)
- WMV (`.wmv`)
- WebM (`.webm`)
- Any format supported by OpenCV

## Error Handling

### Video File Issues
- Validates video file can be opened
- Provides clear error messages
- Suggests corrective actions

### Frame Extraction
- Handles end-of-video gracefully
- Checks frame validity
- Logs progress and errors

### Resource Cleanup
- Properly releases video resources
- Closes video handler on exit
- Handles KeyboardInterrupt (Ctrl+C)

## Future Enhancements (Potential)

1. **Dynamic Sensor Data**
   - Time-based sensor variations
   - CSV file input for sensor data
   - Sensor data interpolation

2. **Advanced Frame Selection**
   - Skip frames based on criteria
   - Motion detection
   - Scene change detection

3. **Multi-Video Processing**
   - Batch process multiple videos
   - Playlist support
   - Directory scanning

4. **Performance Optimization**
   - Multi-threaded frame extraction
   - Frame buffering
   - Compressed frame storage

5. **Enhanced Output**
   - Video annotation
   - Frame metadata overlay
   - Summary statistics

## Testing Checklist

- [x] VideoHandler creates and opens video
- [x] VideoHandler extracts frames correctly
- [x] VideoHandler tracks progress
- [x] VideoHandler closes properly
- [x] StaticSensorHandler returns correct data
- [x] StaticSensorHandler data is consistent
- [x] Integration with MetadataHandler
- [x] Integration with DataFormatter
- [x] Integration with MqttHandler
- [x] Error handling for missing video
- [x] Cleanup on exit
- [x] Documentation complete

## Documentation Files

1. **README.md** - Main project documentation with video mode section
2. **VIDEO_PROCESSING_GUIDE.md** - Detailed quick start guide
3. **config_video_example.py** - Configuration examples
4. **main_video.py** - Inline documentation and docstrings
5. **IMPLEMENTATION_SUMMARY.md** - This file

## Support & Troubleshooting

Common issues and solutions documented in:
- VIDEO_PROCESSING_GUIDE.md (Troubleshooting section)
- main_video.py (Inline comments)
- test_video_components.py (Diagnostic tests)

## Conclusion

The video processing mode provides a flexible, hardware-independent way to use the Edge Data Collector system with pre-recorded video files. It maintains compatibility with the existing infrastructure while adding new capabilities for batch processing, testing, and development.
