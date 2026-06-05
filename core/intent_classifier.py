class IntentClassifier:

    WEBSITE_KEYWORDS = {
        "portfolio": ["portfolio", "resume", "cv", "personal site", "developer"],
        "saas": ["saas", "startup", "dashboard", "software tool"],
        "restaurant": ["restaurant", "restraunt", "food", "cafe", "menu"],
        "ecommerce": [  "ecommerce","e-commerce","online store", "store", "shop","shopping","buy", "product"],
        "blog": ["blog", "articles", "writing", "news", "newsletter"],
        "gym": ["gym", "fitness", "workout", "trainer", "training"]
    }

    def classify(self, prompt: str) -> dict:
        prompt = prompt.lower()

        scores = {}

        for intent, keywords in self.WEBSITE_KEYWORDS.items():
            scores[intent] = sum(1 for kw in keywords if kw in prompt)

        best = max(scores, key=scores.get)

        if scores[best] == 0:
            return {
                "website_type": "generic",
                "confidence": 0
            }

        return {
            "website_type": best,
            "confidence": scores[best] / max(1, sum(scores.values()))
        }