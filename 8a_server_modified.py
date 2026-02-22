"""
server.py

Flask server for EmotionDetection application.
Exposes /emotion_detector endpoint to analyze emotions from text.
"""

import json
from flask import Flask, request, jsonify
from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.route('/emotion_detector', methods=['POST'])
def emotion_detector_endpoint():
    """
    Flask endpoint to analyze emotions of provided text.
    Accepts POST JSON with "text" field.
    Returns JSON with emotion scores and dominant emotion.
    """
    data = request.get_json()
    text = data.get("text", "")

    result_json = emotion_detector(text)
    result_dict = json.loads(result_json)

    # check for dominant emotion
    dominant_emotion = (
        max(result_dict, key=result_dict.get)
        if all(v is not None for v in result_dict.values())
        else None
    )

    if dominant_emotion is None:
        return jsonify({"result": "Invalid text! Please try again!", "details": result_dict}), 400

    result_dict["dominant_emotion"] = dominant_emotion

    response_str = (
        f"For the given statement, the system response is "
        f"'anger': {result_dict.get('anger', 0)}, "
        f"'disgust': {result_dict.get('disgust', 0)}, "
        f"'fear': {result_dict.get('fear', 0)}, "
        f"'joy': {result_dict.get('joy', 0)}, "
        f"and 'sadness': {result_dict.get('sadness', 0)}. "
        f"The dominant emotion is {dominant_emotion}."
    )

    return jsonify({"result": response_str, "details": result_dict})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)