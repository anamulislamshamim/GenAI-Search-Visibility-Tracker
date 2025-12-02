const get_python_code = () => {
    return `
def extract_keywords(text: str) -> List[str]:
    """Very simple keyword extraction."""
    keywords = set(word.lower() for word in text.split() if len(word) > 3 and word.isalpha())
    return list(keywords)[:5]


def get_sentiment_score(text: str) -> float:
    """Sentiment scoring using VADER."""
    scores = sentiment_analyzer.polarity_scores(text)
    return scores["compound"]


def generate_embedding(text: str) -> List[float]:
    """Generate embedding using SentenceTransformer."""
    if not model:
        raise ValueError("Embedding model not initialized")
    return model.encode(text, convert_to_tensor=True).tolist()


def calculate_keyword_match_score(keywords: List[str], brand_name: str, raw_text: str) -> float:
    """
    Keyword Match Score:
    Measures how relevant the extracted keywords are to the brand.
    Simple formula: (#keywords that appear in the response) / total keywords.
    Range: 0 → 1
    """
    if not keywords:
        return 0.0
    matches = sum(1 for k in keywords if k in raw_text.lower())
    return round(matches / len(keywords), 3)


def calculate_brand_frequency(brand_name: str, raw_text: str) -> float:
    """
    Brand Appearance Frequency:
    Count occurrences of brand in text relative to total tokens.
    Range: 0 → 1
    """
    tokens = raw_text.lower().split()
    if not tokens:
        return 0.0
    freq = tokens.count(brand_name.lower()) / len(tokens)
    return round(min(freq * 10, 1.0), 3)  # scaled but capped to 1.0


def calculate_semantic_similarity(raw_text: str, brand_name: str) -> float:
    """
    Semantic similarity between brand and the response using embeddings.
    Range: 0 → 1
    """
    if not model:
        return 0.0
    brand_emb = model.encode(brand_name)
    text_emb = model.encode(raw_text)
    sim = util.cos_sim(brand_emb, text_emb).item()
    return round((sim + 1) / 2, 3)  # map [-1,1] → [0,1]


def calculate_correctness_score(raw_text: str, brand_name: str) -> float:
    """
    A placeholder correctness scoring function.
    You may later expand this using a fact-check prompt or RAG lookup.
    Range: 0 → 1
    """
    # Rule-based placeholder: if brand exists in text → good
    score = 1.0 if brand_name.lower() in raw_text.lower() else 0.3
    return round(score, 3)


def calculate_model_consistency(previous_scores: List[float], current_score: float) -> float:
    """
    Model consistency score:
    Measures how stable LLM answers are for the same brand.
    Range: 0 → 1
    """
    if not previous_scores:
        return 1.0  # no history yet = fully consistent
    diffs = [abs(current_score - s) for s in previous_scores]
    stability = 1 - (sum(diffs) / len(diffs))
    return round(max(min(stability, 1.0), 0.0), 3)


def calculate_visibility_score(
    sentiment_score: float,
    semantic_similarity: float,
    keyword_match: float,
    brand_freq: float,
    correctness: float,
    consistency: float
) -> float:
    """
    Expanded visibility score using weighted formula.
    All values assumed ∈ [0,1].
    Final score mapped to 0-100.
    """

    # Weight selection: balanced & easy to justify
    weights = {
        "sentiment": 0.20,
        "semantic": 0.25,
        "keyword": 0.15,
        "brand_freq": 0.15,
        "correctness": 0.15,
        "consistency": 0.10,
    }

    score = (
        sentiment_score * weights["sentiment"] +
        semantic_similarity * weights["semantic"] +
        keyword_match * weights["keyword"] +
        brand_freq * weights["brand_freq"] +
        correctness * weights["correctness"] +
        consistency * weights["consistency"]
    )

    return round(score * 100, 2)  # Range → 0–100`
}

export default get_python_code