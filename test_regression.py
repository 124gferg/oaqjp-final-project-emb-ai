"""Isolated tests for parsing, request errors, and Flask input handling.

These mocks validate application behavior, not the Watson model's predictions.
"""

import json
import unittest
from unittest.mock import Mock, patch
import requests
from EmotionDetection import emotion_detector
from server import app


class TestRegression(unittest.TestCase):
    """Exercise failure paths without depending on the remote service."""

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_scores_and_dominant_emotion(self, post):
        """Preserve every model score and select the highest-scoring label."""
        scores = {"anger": 0.1, "disgust": 0.2, "fear": 0.3, "joy": 0.9, "sadness": 0.4}
        post.return_value = Mock(
            status_code=200,
            text=json.dumps({"emotionPredictions": [{"emotion": scores}]}),
        )
        self.assertEqual(emotion_detector("hello"), dict(scores, dominant_emotion="joy"))

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_http_400_returns_none(self, post):
        """Return all six required keys with None values after HTTP 400."""
        post.return_value = Mock(status_code=400)
        self.assertEqual(
            emotion_detector(""),
            dict.fromkeys(("anger", "disgust", "fear", "joy", "sadness", "dominant_emotion")),
        )

    @patch("server.emotion_detector")
    def test_blank_input(self, detector):
        """Reject absent and whitespace-only inputs without a remote call."""
        with app.test_client() as client:
            for query in ({}, {"textToAnalyze": "   "}):
                response = client.get("/emotionDetector", query_string=query)
                self.assertEqual(response.get_data(as_text=True), "Invalid text! Please try again!")
        detector.assert_not_called()

    @patch("server.emotion_detector", side_effect=requests.ConnectionError)
    def test_service_failure(self, _detector):
        """Report upstream failure instead of claiming a model prediction."""
        with app.test_client() as client:
            self.assertEqual(client.get("/emotionDetector?textToAnalyze=hello").status_code, 502)

    @patch("server.emotion_detector", return_value={"dominant_emotion": None})
    def test_none_dominant_emotion(self, _detector):
        """Display the required error message for invalid model input."""
        with app.test_client() as client:
            response = client.get("/emotionDetector?textToAnalyze=invalid")
            self.assertEqual(response.get_data(as_text=True), "Invalid text! Please try again!")


if __name__ == "__main__":
    unittest.main()
