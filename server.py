"""Serve the Emotion Detector web interface and its analysis endpoint."""

import requests
from flask import Flask, render_template, request
from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.route("/")
def index():
    """Render the original course-provided interface."""
    return render_template("index.html")


@app.route("/emotionDetector")
def emotion_detector_route():
    """Analyze the input and return the required result or a clear error."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    if not text_to_analyze.strip():
        return "Invalid text! Please try again!"
    try:
        result = emotion_detector(text_to_analyze)
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return "The emotion detection service is unavailable. Please try again!", 502
    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!"
    return (
        f"For the given statement, the system response is 'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, 'fear': {result['fear']}, "
        f"'joy': {result['joy']} and 'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
