from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/get_video_metadata', methods=['POST'])
def get_metadata():
    data = request.get_json()
    video_url = data.get("url")
    if not video_url:
        return jsonify({"error": "Missing video URL"}), 400

    try:
        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_url
        ]
        duration = subprocess.check_output(cmd).decode().strip()
        return jsonify({"duration": float(duration)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

app.run(host="0.0.0.0", port=8080)
