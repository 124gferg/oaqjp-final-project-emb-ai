# Final project

Emotion Detector is a Python and Flask application that analyzes text with the
embeddable Watson NLP EmotionPredict service. It returns anger, disgust, fear,
joy and sadness scores and the dominant emotion.

## Run

Install dependencies with `python3 -m pip install -r requirements.txt`, then run
`python3 server.py` and open http://localhost:5000. The Watson service is provided
by IBM Skills Network and must be reachable from the course lab environment.

## Validate

- Live Watson tests: `python3 -m unittest -v test_emotion_detection.py`
- Isolated regression tests: `python3 -m unittest -v test_regression.py`
- Static analysis: `python3 -m pylint server.py`

The original course frontend and license are retained. The implementation was
prepared with AI assistance and should be reviewed before submission.
