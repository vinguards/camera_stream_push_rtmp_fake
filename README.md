# Camera Stream Push RTMP Fake

This project simulates IP cameras by streaming local video files to an RTMP server in a loop.
It adds a "live" timestamp overlay and supports multiple concurrent streams.

## Prerequisites

- Python 3
- GStreamer 1.0 and plugins (good, bad, ugly, libav)
- Python GObject bindings (`python3-gi`, `python3-gst-1.0`)

### Install Dependencies (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install \
    python3-gi \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav
```

## Configuration

Edit `config.json` to map your UUIDs to video files.
Format:
```json
[
    {
        "uuid": "<your-uuid>",
        "file": "<filename.mp4>"
    }
]
```
The video files should be in the same directory as the script.

## Usage

Run the manager script:
```bash
python3 manager.py
```

This will launch a separate process for each entry in the configuration file.
Each process will:
1. Decode the video.
2. Overlay a dynamic timestamp (fake live feed).
3. Encode to H.264.
4. Push to `rtmp://anhoidong.datacenter.cvedix.com:1935/live/<uuid>`.
5. Restart automatically when the file ends.

## Troubleshooting

- **Missing plugins**: Ensure you have `gstreamer1.0-plugins-bad` (for RTMP) and `gstreamer1.0-libav` (for x264enc if using libav, otherwise `plugins-ugly` usually has x264).
- **Connection Refused**: Check if the RTMP server is reachable and accepting connections.
