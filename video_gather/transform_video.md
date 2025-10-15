ffmpeg -i input.h264 -c copy output.mp4



ffmpeg -i input.h264 -c:v libx264 -c:a aac output.mp4
