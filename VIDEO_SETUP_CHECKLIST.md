# Video Processing Setup Checklist

Use this checklist to ensure you have everything configured correctly before running `main_video.py`.

## Prerequisites
- [ ] Python 3.7 or higher installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] OpenCV installed (`pip install opencv-python`)

## Configuration

### 1. Video File
- [ ] Video file is available and accessible
- [ ] Video file path is correct
- [ ] Video format is supported (MP4, AVI, MOV, MKV, etc.)
- [ ] Video file is not corrupted

### 2. main_video.py Configuration (around line 189)
- [ ] `VIDEO_PATH` updated to point to your video file
- [ ] `CAMERA_ID` set to desired identifier
- [ ] `STATIC_TEMPERATURE` set to desired value (if needed)
- [ ] `STATIC_HUMIDITY` set to desired value (if needed)
- [ ] `STATIC_PRESSURE` set to desired value (if needed)
- [ ] `FRAME_INTERVAL` set to desired processing speed

### 3. config.py Configuration
- [ ] `USE_MQTT` set to `True` or `False` as needed
- [ ] `MQTT_BROKER` configured (if using MQTT)
- [ ] `MQTT_PORT` configured (if using MQTT)
- [ ] `MQTT_TOPIC` configured (if using MQTT)

## Testing

### Quick Test
- [ ] Run `python test_video_components.py` to verify components work
- [ ] Check that test passes without errors

### First Run
- [ ] Run `python main_video.py`
- [ ] Verify video loads successfully
- [ ] Check console output for errors
- [ ] Verify frames are being extracted
- [ ] Check `edge_data_collector/camera/images/` for saved frames

## Troubleshooting

If you encounter issues, check:
- [ ] Video path is absolute or relative to project root
- [ ] Video file has read permissions
- [ ] Sufficient disk space for extracted frames
- [ ] MQTT broker is running (if using MQTT)
- [ ] No firewall blocking MQTT connection (if using MQTT)

## Common Issues

### "Could not open video file"
- Verify VIDEO_PATH is correct
- Check file exists: `ls -l path/to/video.mp4` (Linux/Mac) or `dir path\to\video.mp4` (Windows)
- Try absolute path instead of relative path

### "No module named 'cv2'"
- Install OpenCV: `pip install opencv-python`
- Verify installation: `python -c "import cv2; print(cv2.__version__)"`

### "Permission denied"
- Check file permissions
- Run with appropriate user permissions
- Move video to accessible location

### MQTT Connection Failed
- Verify MQTT broker is running
- Check broker address and port
- Test connection: `telnet localhost 1883` (or your broker address)

## Ready to Run!

Once all items are checked:
```bash
python main_video.py
```

Press `Ctrl+C` to stop processing at any time.

## Next Steps

After successful run:
- [ ] Review extracted frames in `edge_data_collector/camera/images/`
- [ ] Check MQTT messages (if enabled)
- [ ] Adjust `FRAME_INTERVAL` if needed
- [ ] Modify sensor values if needed
- [ ] Process additional videos

## Documentation References

- **Quick Start**: VIDEO_PROCESSING_GUIDE.md
- **Configuration Examples**: config_video_example.py
- **Implementation Details**: IMPLEMENTATION_SUMMARY.md
- **Main README**: README.md
