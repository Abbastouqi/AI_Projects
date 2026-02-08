from typing import List, Dict
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI
from src.config import Config

class CandidateRanker:
    """Rank candidates based on job description similarity."""
    
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.EMBEDDING_MODEL

    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for text using OpenAI."""
        try:
            text = text.replace("\n", " ")
            return self.client.embeddings.create(input=[text], model=self.model).data[0].embedding
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return [0.0] * 1536

    def rank_candidates(self, job_description: str, candidates: List[Dict]) -> List[Dict]:
        """Rank candidates by similarity to job description."""
        if not candidates:
            return []

        # Get job embedding
        job_embedding = self.get_embedding(job_description)
        
        ranked_candidates = []
        
        for candidate in candidates:
            # Combine candidate text fields
            candidate_text = f"{candidate.get('skills', '')} {candidate.get('experience_years', '')} {candidate.get('education', '')} {candidate.get('full_text', '')}"
            
            # Get candidate embedding
            cand_embedding = self.get_embedding(candidate_text)
            
            # Calculate similarity
            similarity = cosine_similarity(
                [job_embedding], 
                [cand_embedding]
            )[0][0]
            
            ranked_candidates.append({
                **candidate,
                "ranking_score": float(similarity),
                "text_match": float(similarity),
                "skill_match": float(similarity), # Simplified for this example
                "experience_match": float(similarity) # Simplified
            })
        
        # Sort by score descending
        ranked_candidates.sort(key=lambda x: x['ranking_score'], reverse=True)
        
        # Add rank numbers
        for i, cand in enumerate(ranked_candidates, 1):
            cand['rank'] = i
            
        return ranked_candidates