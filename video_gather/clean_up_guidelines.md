## Cleanup Guide
Disable auto-startup and shutdown after field use. Keeps script and videos intact. Run via SSH.


Run this script: 
bash video_gather/cleanup_video_capturing_mode



1. **Disable Auto-Run**:
   ```
   sudo systemctl stop record-video.service
   sudo systemctl disable record-video.service
   sudo rm /etc/systemd/system/record-video.service
   sudo systemctl daemon-reload
   ```

2. **Revert Permissions** (Recommended for Security):
   ```
   sudo visudo
   ```
   - Delete the line: `pi-collector ALL=(ALL) NOPASSWD: /sbin/shutdown`
   - Save/exit.

3. **Final Steps**:
   ```
   sudo reboot
   ```
   - Pi now boots normally (no auto-run/shutdown).
   - Verify: `sudo systemctl status record-video.service` (should fail/not found).

Script and videos remain at `/home/pi-collector/edge_data_processor/video_gather/` for future manual use.