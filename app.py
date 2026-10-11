
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = FastAPI(title="Batch Sentiment Analysis")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

analyzer = SentimentIntensityAnalyzer()


class SentimentRequest(BaseModel):
    sentences: list[str] = Field(min_length=1)


@app.get("/")
def root():
    return {"message": "Sentiment API is running"}


@app.post("/sentiment")
def analyze_sentiment(request: SentimentRequest):
    results = []

    for sentence in request.sentences:
        scores = analyzer.polarity_scores(sentence)
        compound = scores["compound"]

        if compound >= 0.05:
            sentiment = "happy"
        elif compound <= -0.05:
            sentiment = "sad"
        else:
            sentiment = "neutral"

        results.append({
            "sentence": sentence,
            "sentiment": sentiment
        })

    return {"results": results}
