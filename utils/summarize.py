from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_summary(text, length="medium"):
    text = text.strip()
    if len(text.split()) < 10:
        return text

    max_length = {"short": 50, "medium": 100, "long": 200}.get(length, 100)
    min_length = max(25, max_length // 2)

    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
    return summary.strip()
