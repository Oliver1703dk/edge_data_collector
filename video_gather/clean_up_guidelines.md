Stop Guide (Mid-Run Intervention)
If you need to halt recording/shutdown (e.g., testing with peripherals or error).

During Boot/Recording (With Monitor/Keyboard):

Power on, auto-logs to shell (~10-15s post-boot).
Quickly type: sudo systemctl stop record-video.service (stops script; no shutdown).
Or manually: pkill -f record_video.py (kills Python process).


Headless (via SSH):

SSH in during boot window: ssh pi-collector@raspberrypi.local, then sudo systemctl stop record-video.service.
To skip next boot: sudo systemctl disable record-video.service (re-enable later).


If Shutdown Starts:

Unplug (safe, as it's flushing). Power on and stop as above.



For one-off manual run: python3 /home/pi-collector/edge_data_processor/video_gather/record_video.py (no auto-shutdown unless you add it).
Cleanup Guide
Revert Pi to stock after field use (office/normal mode). This disables auto-startup and shutdown but keeps the script and videos intact. Do via SSH or peripherals.

Disable Auto-Run:
textsudo systemctl stop record-video.service
sudo systemctl disable record-video.service
sudo rm /etc/systemd/system/record-video.service
sudo systemctl daemon-reload

Revert Permissions:

sudo visudo, delete pi-collector ALL=(ALL) NOPASSWD: /sbin/shutdown line, save/exit.


Final Steps:

Reboot: sudo reboot—boots normally.
Verify: sudo systemctl status record-video.service (should fail/not found).



Pi is now reset to pre-setup behavior (no auto-run/shutdown). Script and videos remain at /home/pi-collector/edge_data_processor/video_gather/ for future use. Re-flash SD if major issues.