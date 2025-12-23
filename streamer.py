import sys
import time
import signal
import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, GLib

def run_stream(file_path, rtmp_url, uuid):
    Gst.init(None)

    # Convert file path to absolute if needed, GStreamer likes absolute paths or file:// URIs,
    # but filesrc location=... works with standard paths.

    # Pipeline construction
    # We use decodebin to handle various containers.
    # We add timeoverlay for a realistic effect.
    # We enforce h264 encoding for RTMP.
    
    pipeline_str = (
        f'filesrc location="{file_path}" ! '
        'decodebin ! '
        'videoconvert ! '
        f'timeoverlay valignment=top halignment=right text="CAM: {uuid}" font-desc="Sans, 20" ! '
        'videoconvert ! '
        'x264enc bitrate=2500 tune=zerolatency speed-preset=superfast key-int-max=60 ! '
        'h264parse ! '
        'flvmux streamable=true ! '
        f'rtmpsink location="{rtmp_url} live=1"'
    )

    print(f"Starting stream for {uuid}...")
    # print(f"Pipeline: {pipeline_str}")

    pipeline = Gst.parse_launch(pipeline_str)
    
    bus = pipeline.get_bus()
    
    # Start playing
    ret = pipeline.set_state(Gst.State.PLAYING)
    if ret == Gst.StateChangeReturn.FAILURE:
        print("ERROR: Unable to set the pipeline to the playing state.")
        return False

    # Wait until error or EOS
    msg = bus.timed_pop_filtered(
        Gst.CLOCK_TIME_NONE, 
        Gst.MessageType.ERROR | Gst.MessageType.EOS
    )

    if msg:
        if msg.type == Gst.MessageType.ERROR:
            err, debug = msg.parse_error()
            print(f"Error received from element {msg.src.get_name()}: {err.message}")
            print(f"Debugging information: {debug}")
        elif msg.type == Gst.MessageType.EOS:
            print("End-Of-Stream reached.")
    
    # Cleanup
    pipeline.set_state(Gst.State.NULL)
    return True

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 streamer.py <video_file> <uuid>")
        sys.exit(1)

    video_file = sys.argv[1]
    my_uuid = sys.argv[2]
    rtmp_base = "rtmp://anhoidong.datacenter.cvedix.com:1935/live"
    rtmp_url = f"{rtmp_base}/{my_uuid}"

    # Loop forever
    while True:
        success = run_stream(video_file, rtmp_url, my_uuid)
        if not success:
            print("Stream failed unexpectedly. Retrying in 5 seconds...")
            time.sleep(5)
        # Verify quick loop restart
        # time.sleep(0.1) 

if __name__ == "__main__":
    main()
