import json
from typing import Dict, Tuple
from openai import OpenAI
from src.config import Config

class CandidateScreener:
    """Automated candidate screening using OpenAI API."""
    
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.MODEL_NAME
    
    def screen_candidate(self, candidate_info: Dict, job_requirements: str = None) -> Tuple[float, str]:
        """
        Screen candidate against job requirements.
        Returns (score, feedback)
        """
        if job_requirements is None:
            job_requirements = self._get_default_requirements()
        
        prompt = self._create_screening_prompt(candidate_info, job_requirements)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert recruiter evaluating candidates."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            result_text = response.choices[0].message.content
            score, feedback = self._parse_screening_response(result_text)
            
            return score, feedback
        
        except Exception as e:
            print(f"Error screening candidate: {str(e)}")
            return self._fallback_screening(candidate_info, job_requirements)
    
    def _create_screening_prompt(self, candidate_info: Dict, job_requirements: str) -> str:
        """Create screening prompt for OpenAI."""
        candidate_text = self._format_candidate_info(candidate_info)
        
        prompt = f"""
You are screening a candidate for a job position.

CANDIDATE INFORMATION:
{candidate_text}

JOB REQUIREMENTS:
{job_requirements}

Please evaluate the candidate on a scale of 0-1 (0 = not suitable, 1 = perfect match).

Provide your response in this exact format:
SCORE: 0.XX
FEEDBACK: [Your detailed feedback here]

Consider:
1. Skill match with job requirements
2. Experience level appropriateness
3. Educational background
4. Overall fit for the role
"""
        return prompt
    
    def _format_candidate_info(self, candidate_info: Dict) -> str:
        """Format candidate information for the prompt."""
        lines = []
        
        if 'name' in candidate_info:
            lines.append(f"Name: {candidate_info['name']}")
        
        if 'email' in candidate_info:
            lines.append(f"Email: {candidate_info['email']}")
        
        if 'phone' in candidate_info:
            lines.append(f"Phone: {candidate_info['phone']}")
        
        if 'skills' in candidate_info and candidate_info['skills']:
            lines.append(f"Skills: {', '.join(candidate_info['skills'])}")
        
        if 'experience_years' in candidate_info:
            lines.append(f"Years of Experience: {candidate_info['experience_years']}")
        
        if 'education' in candidate_info and candidate_info['education']:
            lines.append(f"Education: {', '.join(candidate_info['education'])}")
        
        return '\n'.join(lines)
    
    def _parse_screening_response(self, response_text: str) -> Tuple[float, str]:
        """Parse OpenAI response to extract score and feedback."""
        lines = response_text.split('\n')
        
        score = 0.5
        feedback = response_text
        
        for line in lines:
            if 'SCORE:' in line:
                try:
                    score_str = line.split('SCORE:')[1].strip()
                    score = float(score_str)
                    score = max(0.0, min(1.0, score))  # Clamp between 0 and 1
                except:
                    pass
            
            if 'FEEDBACK:' in line:
                feedback = line.split('FEEDBACK:')[1].strip()
        
        return score, feedback
    
    def _fallback_screening(self, candidate_info: Dict, job_requirements: str) -> Tuple[float, str]:
        """Fallback screening when API is unavailable."""
        score = 0.5
        feedback_parts = []
        
        # Check skills match
        if 'skills' in candidate_info and candidate_info['skills']:
            score += 0.1
            feedback_parts.append(f"Has {len(candidate_info['skills'])} relevant skills")
        
        # Check experience
        exp_years = candidate_info.get('experience_years', 0)
        if exp_years > 3:
            score += 0.2
            feedback_parts.append(f"{int(exp_years)} years of experience")
        elif exp_years > 0:
            score += 0.1
        
        # Check education
        if 'education' in candidate_info and candidate_info['education']:
            score += 0.1
            feedback_parts.append("Has relevant education")
        
        score = min(score, 1.0)
        feedback = "Fallback evaluation: " + ", ".join(feedback_parts) if feedback_parts else "Basic evaluation"
        
        return score, feedback
    
    def _get_default_requirements(self) -> str:
        """Default job requirements if none provided."""
        return """
- Strong programming skills in Python or similar languages
- 2+ years of professional experience
- Knowledge of data structures and algorithms
- Experience with version control systems
- Good communication and teamwork skills
- Bachelor's degree in Computer Science or related field
"""
