import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from transformers import pipeline

class LLMProcessor:
    def __init__(self):
        self.classifier = pipeline(
            "zero-shot-classification",
            model="typeform/distilbert-base-uncased-mnli",
            tokenizer_kwargs={"clean_up_tokenization_spaces": True}
        )
    
    def preprocess_query(self, query):
        query = query.lower()
        if "регион" in query and "доход" in query and ("наибольший" in query or "высший" in query):
            return f"find region with highest average earnings {query}"
        elif "криптовалюта" in query and "доход" in query:
            return f"compare cryptocurrency earnings {query}"
        elif "регион" in query and "распредел" in query:
            return f"distribution of earnings by client region {query}"
        elif "эксперт" in query and ("проект" in query or "работ" in query):
            return f"expert freelancers project statistics {query}"
        elif "криптовалюта" in query and ("процент" in query or "доля" in query):
            return f"percentage of cryptocurrency payment usage {query}"
        return query
    
    def process_query(self, query):
        preprocessed = self.preprocess_query(query)
        candidate_labels = [
            "compare cryptocurrency payment earnings",
            "distribution of earnings by client region",
            "expert freelancers project statistics",
            "region with highest average earnings",
            "percentage of cryptocurrency payment usage",
            "unknown"
        ]
        result = self.classifier(preprocessed, candidate_labels, multi_label=False)
        return result['labels'][0]