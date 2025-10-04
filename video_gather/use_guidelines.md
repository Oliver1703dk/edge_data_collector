## Use Guide
For vehicle-mounted flood detection captures (headless).

1. **Prep**:
   - Secure Pi + camera in weatherproof case on vehicle (wide-angle lens for fields).
   - Use 10000mAh+ power bank (5V/3A USB-C). Expect 50+ cycles per charge.
   - Label sessions mentally (e.g., flooded/dry) for later sorting by timestamp.

2. **Field Workflow**:
   - Position vehicle in field (flooded, dry, etc.).
   - Plug in power: Pi boots (~20s), auto-records 30s video (camera LED blinks), saves to `/home/pi-collector/edge_data_processor/video_gather/videos/`, auto-shuts down (~10s).
   - Total per clip: ~60s. Unplug after shutdown (safe).
   - Repeat: Reposition, plug in for next clip. Files auto-name by date/time (e.g., `flood_video_20251004_143022.h264`).

3. **Monitoring**:
   - LED: Blinks green during record; stops on save/shutdown.
   - Battery: Swap if low; test runtime at home.

4. **Post-Use**:
   - Eject SD/USB on computer, copy videos. Convert/view with VLC or `ffmpeg`.