from flask import Flask, request
from EmotionDetection.emotion_detection import emotion_detector
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "Emotion Detection API is running!"

@app.route("/emotionDetector")
def emotion_detector_route():
    text = request.args.get('text')

    result = emotion_detector(text)
    result_dict = json.loads(result)

    if result_dict["dominant_emotion"] is None:
        return "Invalid text! Please try again!"

    response = (
        f"For the given statement, the system response is "
        f"'anger': {result_dict['anger']}, "
        f"'disgust': {result_dict['disgust']}, "
        f"'fear': {result_dict['fear']}, "
        f"'joy': {result_dict['joy']}, "
        f"and 'sadness': {result_dict['sadness']}. "
        f"The dominant emotion is {result_dict['dominant_emotion']}."
    )

    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
