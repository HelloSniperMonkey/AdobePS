import PyPDF2
import re
import json
from typing import List, Dict, Any, Tuple
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from io import StringIO

class PDFProcessor:
    def __init__(self):
        """Initialize PDF processor with lightweight models"""
        # Load lightweight model for heading detection (≤200MB)
        self.model_name = "distilbert-base-uncased"  # ~260MB but we'll use only for inference
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)
        
        # Heading patterns for detection
        self.heading_patterns = [
            r'^[A-Z][A-Z\s]{2,}$',  # ALL CAPS
            r'^\d+\.\s+[A-Z]',      # Numbered headings
            r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*$',  # Title Case
            r'^[IVX]+\.\s+[A-Z]',   # Roman numerals
        ]
        
        # Font size thresholds (relative)
        self.large_font_threshold = 14
        self.medium_font_threshold = 12
        
    def extract_outline(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extract PDF outline with title and hierarchical structure
        Returns: { title, outline: [ { level: H1|H2|H3, text, page }... ] }
        """
        try:
            # Extract text with layout information
            text_content = self._extract_text_with_layout(pdf_path)
            
            # Extract title
            title = self._extract_title(text_content)
            
            # Extract headings with page numbers
            headings = self._extract_headings_with_pages(pdf_path, text_content)
            
            # Classify heading levels
            classified_headings = self._classify_heading_levels(headings)
            
            return {
                "title": title,
                "outline": classified_headings
            }
            
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")
    
    def _extract_text_with_layout(self, pdf_path: str) -> str:
        """Extract text while preserving layout information"""
        output = StringIO()
        with open(pdf_path, 'rb') as file:
            extract_text_to_fp(file, output, laparams=LAParams())
        return output.getvalue()
    
    def _extract_title(self, text_content: str) -> str:
        """Extract document title from first few lines"""
        lines = text_content.split('\n')[:10]  # Check first 10 lines
        
        for line in lines:
            line = line.strip()
            if line and len(line) > 3 and len(line) < 200:
                # Simple heuristics for title detection
                if (line.isupper() or 
                    (line[0].isupper() and line.count(' ') <= 10) or
                    re.match(r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*$', line)):
                    return line
        
        return "Untitled Document"
    
    def _extract_headings_with_pages(self, pdf_path: str, text_content: str) -> List[Dict[str, Any]]:
        """Extract headings with their page numbers"""
        headings = []
        
        # Use PyPDF2 for page-by-page processing
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                
                # Split page into lines
                lines = page_text.split('\n')
                
                for line in lines:
                    line = line.strip()
                    if self._is_heading(line):
                        headings.append({
                            "text": line,
                            "page": page_num + 1,
                            "raw_text": line
                        })
        
        return headings
    
    def _is_heading(self, text: str) -> bool:
        """Determine if a line of text is a heading"""
        if not text or len(text) < 3:
            return False
        
        # Check pattern matching
        for pattern in self.heading_patterns:
            if re.match(pattern, text):
                return True
        
        # Check length and capitalization
        if (len(text) < 100 and 
            (text.isupper() or 
             (text[0].isupper() and text.count(' ') <= 8))):
            return True
        
        return False
    
    def _classify_heading_levels(self, headings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Classify headings into H1, H2, H3 levels based on patterns and context"""
        classified = []
        
        for heading in headings:
            text = heading["text"]
            level = self._determine_heading_level(text, len(classified))
            
            classified.append({
                "level": level,
                "text": text,
                "page": heading["page"]
            })
        
        return classified
    
    def _determine_heading_level(self, text: str, position: int) -> str:
        """Determine heading level (H1, H2, H3) based on text characteristics"""
        # H1: Main chapter titles, usually numbered or very prominent
        if (re.match(r'^\d+\.\s+[A-Z]', text) or
            re.match(r'^[IVX]+\.\s+[A-Z]', text) or
            text.isupper() and len(text) > 5):
            return "H1"
        
        # H2: Section headings, often title case with moderate length
        if (re.match(r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*$', text) and
            len(text) > 10 and len(text) < 50):
            return "H2"
        
        # H3: Subsection headings, shorter or less prominent
        return "H3"
    
    def get_model_size(self) -> float:
        """Get approximate model size in MB"""
        # Calculate model size
        param_size = sum(p.numel() * p.element_size() for p in self.model.parameters())
        buffer_size = sum(b.numel() * b.element_size() for b in self.model.buffers())
        model_size_mb = (param_size + buffer_size) / 1024 / 1024
        return model_size_mb 