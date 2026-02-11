"""
Document Handler Skill
Creates and manages documents
"""

import os
from datetime import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class DocumentHandler:
    def __init__(self, default_path: str = "./documents"):
        self.default_path = default_path
        os.makedirs(default_path, exist_ok=True)
    
    def create_document(self, filename: str, content: str, **kwargs) -> Dict[str, Any]:
        """Create a text document"""
        try:
            if not filename.endswith(('.txt', '.md')):
                filename += '.txt'
            
            filepath = os.path.join(self.default_path, filename)
            
            full_content = f"Created by AI Agent on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            full_content += "="*50 + "\n\n"
            full_content += content
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(full_content)
            
            return {
                'status': 'success',
                'filename': filename,
                'filepath': os.path.abspath(filepath),
                'message': f'Document "{filename}" created'
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def list_documents(self) -> Dict[str, Any]:
        """List documents"""
        try:
            files = os.listdir(self.default_path)
            docs = [f for f in files if f.endswith(('.txt', '.md'))]
            
            return {
                'status': 'success',
                'count': len(docs),
                'documents': docs
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

if __name__ == "__main__":
    dh = DocumentHandler()
    print(dh.create_document("test.txt", "Hello World"))
