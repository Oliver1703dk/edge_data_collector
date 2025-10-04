Setup Guide
This is a one-time headless setup (no monitor/keyboard after flashing). Assumes Raspberry Pi 4/5 or Zero 2 W with Camera Module connected. Username: pi-collector.

Prepare SD Card:

Download Raspberry Pi OS Lite (64-bit) from raspberrypi.com/software.
Use Raspberry Pi Imager to flash it to a 16GB+ high-endurance SD card (e.g., SanDisk Extreme).
In Imager's advanced settings: Enable SSH, set username/password (e.g., pi-collector/yourpassword), configure WiFi if needed.


Initial Boot and Config (Headless via SSH):

Insert SD, connect camera to CSI port, power on Pi (Ethernet or WiFi for access).
SSH from your computer: ssh pi-collector@raspberrypi.local (or IP from router).
Update system: sudo apt update && sudo apt upgrade -y.
Enable camera: sudo raspi-config > Interface Options > Camera > Enable > Finish > Reboot.
Install dependencies: sudo apt install python3-picamera2 ffmpeg -y.
Enable passwordless shutdown: sudo visudo, add pi-collector ALL=(ALL) NOPASSWD: /sbin/shutdown at end, save/exit.


Deploy Script and Auto-Start:

Create directory: mkdir -p /home/pi-collector/edge_data_processor/video_gather.
Create script: nano /home/pi-collector/edge_data_processor/video_gather/record_video.py, paste the code above, save (Ctrl+O, Enter, Ctrl+X).
Make executable: chmod +x /home/pi-collector/edge_data_processor/video_gather/record_video.py.
Create systemd service: sudo nano /etc/systemd/system/record-video.service, paste:
text[Unit]
Description=Record 30s Video on Boot
After=multi-user.target

[Service]
Type=oneshot
User=pi-collector
ExecStart=/usr/bin/python3 /home/pi-collector/edge_data_processor/video_gather/record_video.py --duration 30
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
Save/exit.
Enable: sudo systemctl daemon-reload && sudo systemctl enable record-video.service.
Test: sudo reboot, SSH back, check ls /home/pi-collector/edge_data_processor/video_gather/videos/ for file. Play: ffplay flood_video_*.h264.


Optional USB Storage:

Plug USB drive, identify: lsblk.
Format: sudo mkfs.ext4 /dev/sda1.
Auto-mount: blkid /dev/sda1 (note UUID), sudo nano /etc/fstab, add UUID=XXXX /mnt/usb ext4 defaults 0 2. Save.
Update service: Edit ExecStart to --folder /mnt/usb/videos, then sudo systemctl daemon-reload.



Reboot and verify—no issues? Ready for field.