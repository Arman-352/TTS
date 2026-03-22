from TTS.api import TTS
import os
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

# Load high-quality model
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

VOICE_PRESETS = {
    "default": None,
    "narrator": "voices/narrator.wav",
    "female": "voices/female.wav",
    "deep": "voices/deep.wav"
}

@app.route("/speak", methods=["POST"])
def speak():
    data = request.json

    text = data.get("text", "")
    voice_type = data.get("voice", "default")

    speaker = VOICE_PRESETS.get(voice_type)
    output_path = os.path.join(OUTPUT_DIR, "output.wav")

    try:
        tts.tts_to_file(
            text=text,
            file_path=output_path,
            speaker_wav=speaker,
            language="en"
        )

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/")
def home():
    return "Professional AI TTS is running 🚀"

if __name__ == "__main__":
    app.run(debug=True)
