## Setup Guide

Assumes your Pi is already running Debian GNU/Linux 12 (Raspberry Pi OS Bookworm) with camera connected and SSH access as `pi-collector`. Connect via SSH and run these steps.

1. **Install Dependencies**:
   ```
   sudo apt update
   sudo apt install python3-picamera2 ffmpeg -y
   ```

2. **Enable Camera (If Not Already)**:
   ```
   sudo raspi-config
   ```
   - Go to Interface Options > Camera > Enable > Finish > Reboot.

3. **Deploy Script and Directory**:
   ```
   mkdir -p /home/pi-collector/edge_data_processor/video_gather
   nano /home/pi-collector/edge_data_processor/video_gather/record_video.py
   ```
   - Paste the script code above, save (Ctrl+O, Enter, Ctrl+X).
   ```
   chmod +x /home/pi-collector/edge_data_processor/video_gather/record_video.py
   ```

4. **Enable Passwordless Shutdown**:
   ```
   sudo visudo
   ```
   - Add this line at the end: `pi-collector ALL=(ALL) NOPASSWD: /sbin/shutdown`
   - Save/exit.

5. **Set Up Auto-Start on Boot**:
   ```
   sudo nano /etc/systemd/system/record-video.service
   ```
   - Paste this:
     ```
     [Unit]
     Description=Record 30s Video on Boot
     After=multi-user.target

     [Service]
     Type=oneshot
     User=pi-collector
     ExecStart=/usr/bin/python3 /home/pi-collector/edge_data_processor/video_gather/record_video.py --duration 30
     RemainAfterExit=yes

     [Install]
     WantedBy=multi-user.target
     ```
   - Save/exit.
   ```
   sudo systemctl daemon-reload
   sudo systemctl enable record-video.service
   ```

6. **Test**:
   ```
   sudo reboot
   ```
   - SSH back in, check `ls /home/pi-collector/edge_data_processor/video_gather/videos/` for the file.
   - Play: `ffplay flood_video_*.h264`.

7. **Optional USB Storage**:
   - Plug USB drive, identify: `lsblk`.
   - Format: `sudo mkfs.ext4 /dev/sda1`.
   - Auto-mount: `blkid /dev/sda1` (note UUID), `sudo nano /etc/fstab`, add `UUID=XXXX /mnt/usb ext4 defaults 0 2`. Save.
   - Update service: Edit `ExecStart` to include `--folder /mnt/usb/videos`, then `sudo systemctl daemon-reload`.

Ready for field use.