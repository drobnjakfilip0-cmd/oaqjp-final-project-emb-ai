@app.route('/emotionDetector', methods=['POST'])
def emotionDetector():
    data = request.get_json()
    text = data.get("text", "")
    
    result_json = emotion_detector(text)
    result_dict = json.loads(result_json)
    
    # proveri dominantnu emociju
    dominant_emotion = max(result_dict, key=result_dict.get) if all(v is not None for v in result_dict.values()) else None
    
    if dominant_emotion is None:
        return jsonify({"result": "Invalid text! Please try again!", "details": result_dict}), 400
    
    result_dict["dominant_emotion"] = dominant_emotion
    
    response_str = (
        f"For the given statement, the system response is "
        f"'anger': {result_dict.get('anger',0)}, "
        f"'disgust': {result_dict.get('disgust',0)}, "
        f"'fear': {result_dict.get('fear',0)}, "
        f"'joy': {result_dict.get('joy',0)}, "
        f"and 'sadness': {result_dict.get('sadness',0)}. "
        f"The dominant emotion is {dominant_emotion}."
    )
    
    return jsonify({"result": response_str, "details": result_dict})