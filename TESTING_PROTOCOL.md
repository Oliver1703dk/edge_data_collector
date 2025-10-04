# Field Video Capture Testing Protocol

Use this protocol whenever you prepare, execute, and validate video collection trips with the Raspberry Pi capture rig. It ensures every recording session is traceable, recoverable, and ready for ingestion by the processing pipeline.

## 1. Objectives
- Confirm the capture script records continuously on boot and segments footage safely.
- Maintain a repeatable method for tagging footage by location without a keyboard or display.
- Protect media from corruption during power cycles or unexpected shutdowns.

## 2. Pre-Field Checklist (Bench Test)
1. **Update software**: Pull the latest repository changes and deploy the current `video-gather/capture_video.py` to `/home/pi/edge_data_processor/`.
2. **Verify dependencies**: Ensure Picamera2 and project requirements are installed inside the active virtual environment.
3. **Service health**: `sudo systemctl status edge-video.service` should report `active (running)` after a reboot.
4. **Storage check**: Confirm the target directory (e.g., `/home/pi/videos`) is mounted and has >10 GB free.
5. **Button/GPIO test**: Press the shutdown/control button to confirm the Pi halts cleanly and that a reboot resumes recording.
6. **Dry run**: Record at least one segment indoors, then inspect the output directory to ensure MP4 files open and logs show segment boundaries.

_Note: Document any configuration overrides (for example, `location_tag=greenhouse_north`) in the lab notebook before leaving._

## 3. Field Deployment Procedure
1. **Power-on**: Connect the capture rig to its battery pack or field power. Wait ~20 seconds for the service to start.
2. **Heartbeat check**: Observe the status LED or heartbeat file (`/tmp/edge-video.status`) to confirm recording has begun.
3. **Location tagging**:
   - If the service reads a site tag from an environment file (for example `/etc/default/edge-video`), edit that file to set `LOCATION_TAG=<site>` and run `sudo systemctl restart edge-video`.
   - If you launch the recorder manually for each site, stop the service (`sudo systemctl stop edge-video`) and run the script with the flag you need: `python3 /home/pi/edge_data_processor/video-gather/capture_video.py --location <site>`.
   - If a physical toggle/rotary switch selects locations, set the switch to the new site before rebooting; confirm the log reflects the correct tag.
4. **Capture window**: Leave the rig running for the planned sampling duration (default segments are 5 minutes). Avoid moving the Pi mid-segment to prevent vibration artifacts.
5. **Environmental notes**: Record weather, lighting, and anomalies in the field logbook with timestamps to correlate with captured video.

## 4. Moving Between Locations
1. Request a controlled stop (GPIO long-press or `sudo systemctl stop edge-video`). Wait for the status indicator to signal the encoder has closed.
2. Update the location tag (flag, switch, or config file).
3. Power-cycle or restart the service; confirm the new folder (`/home/pi/videos/YYYY-MM-DD/<location_tag>/`) appears after the first segment completes.
4. Repeat the deployment procedure for the new site.

## 5. Shutdown and Data Handling
1. Issue `sudo shutdown -h now` via the button or SSH. Do **not** unplug until the status LED goes dark.
2. Remove storage media or leave powered off until back at base.
3. Back at the workstation:
   - Mount the storage volume read-only.
   - Copy footage to the analysis storage with `rsync --progress`.
   - Generate checksums (e.g., `shasum *.mp4`) to verify transfer integrity.
   - Archive the day’s log file (`/home/pi/edge_data_processor/logs/field_capture.log`).

## 6. Post-Field Validation
- Spot-check one segment per location to ensure playback works and timestamps match field notes.
- Confirm disk cleanup retained the expected number of segments; investigate if older clips were trimmed unexpectedly.
- Update the project tracker with site tags, segment counts, total runtime, and any hardware issues.

## 7. Contingency Actions
- **Unexpected power loss**: On reboot, inspect the last segment for corruption. If damaged, note the time gap and rerun the location if feasible.
- **Storage near capacity**: SSH in and remove the oldest dated directories from `/home/pi/videos` after copying them off-device; leave at least the minimum free space configured in the recorder before restarting.
- **Camera failure**: Restart the service; if unresolved, swap to the backup camera module kept in the field kit.

By following this protocol each trip, field footage remains consistent, easy to organize, and ready for downstream processing without surprises.
