import json
import re
from typing import Dict, List
from pathlib import Path
import PyPDF2

class ResumeParser:
    """Parse resumes and extract key information."""
    
    def __init__(self):
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'\b(?:\+1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b'
    
    def parse_resume(self, file_path: str) -> Dict:
        """Parse resume file and extract information."""
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.pdf':
            text = self._extract_pdf_text(file_path)
        elif file_ext in ['.doc', '.docx']:
            text = self._extract_docx_text(file_path)
        elif file_ext == '.txt':
            text = self._extract_txt_text(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
        
        return self._extract_information(text)
    
    def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF file."""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
        return text
    
    def _extract_docx_text(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        from docx import Document
        doc = Document(file_path)
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    
    def _extract_txt_text(self, file_path: str) -> str:
        """Extract text from TXT file."""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            return file.read()
    
    def _extract_information(self, text: str) -> Dict:
        """Extract structured information from resume text."""
        return {
            "email": self._extract_email(text),
            "phone": self._extract_phone(text),
            "name": self._extract_name(text),
            "skills": self._extract_skills(text),
            "experience_years": self._estimate_experience(text),
            "education": self._extract_education(text),
            "full_text": text
        }
    
    def _extract_email(self, text: str) -> str:
        """Extract email address from resume."""
        matches = re.findall(self.email_pattern, text)
        return matches[0] if matches else "Not found"
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone number from resume."""
        matches = re.findall(self.phone_pattern, text)
        if matches:
            return f"({matches[0][0]}) {matches[0][1]}-{matches[0][2]}"
        return "Not found"
    
    def _extract_name(self, text: str) -> str:
        """Extract name from resume (first lines)."""
        lines = text.split('\n')
        for line in lines[:5]:
            if len(line.strip()) > 3 and not any(char.isdigit() for char in line[:10]):
                return line.strip()
        return "Not found"
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume."""
        common_skills = [
            'Python', 'Java', 'JavaScript', 'C++', 'C#', 'SQL', 'HTML', 'CSS',
            'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'FastAPI',
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Git', 'Linux',
            'Machine Learning', 'Deep Learning', 'Data Analysis', 'Big Data',
            'Agile', 'Scrum', 'DevOps', 'CI/CD', 'REST API', 'GraphQL',
            'MongoDB', 'PostgreSQL', 'MySQL', 'Redis', 'Elasticsearch',
            'Product Management', 'Project Management', 'Leadership', 'Communication'
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in common_skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def _extract_education(self, text: str) -> List[str]:
        """Extract education information from resume."""
        education_keywords = ['bachelor', 'master', 'phd', 'diploma', 'degree', 
                            'b.s', 'b.a', 'm.s', 'm.a', 'mba']
        education = []
        
        text_lower = text.lower()
        for keyword in education_keywords:
            if keyword in text_lower:
                education.append(keyword.title())
        
        return list(set(education))
    
    def _estimate_experience(self, text: str) -> float:
        """Estimate years of experience from resume."""
        # Look for year ranges and calculate total experience
        year_pattern = r'20\d{2}\s*-\s*(20\d{2}|present|current)'
        matches = re.findall(year_pattern, text, re.IGNORECASE)
        
        total_years = 0
        for match in matches:
            if 'present' in match.lower() or 'current' in match.lower():
                total_years += 1
            else:
                try:
                    start = int(re.search(r'20\d{2}', text[max(0, text.find(match)-20):text.find(match)]).group())
                    end = int(match.split('-')[1].strip()[:4])
                    total_years += max(0, end - start)
                except:
                    pass
        
        return min(total_years, 60)  # Cap at 60 years
