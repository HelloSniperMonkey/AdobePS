import json
import time
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from pdf_processor import PDFProcessor

class PersonaAnalyzer:
    def __init__(self):
        """Initialize persona analyzer with sentence transformer model"""
        # Load sentence transformer model (≤1GB constraint)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # ~90MB model
        self.pdf_processor = PDFProcessor()
        
    def analyze(self, pdf_files: List[str], persona_description: str, job_to_be_done: str) -> Dict[str, Any]:
        """
        Round 1B: Persona-driven analysis
        Input: 3-10 related PDFs + persona description + job-to-be-done
        Output: JSON with metadata, extracted sections, and sub-section analyses
        """
        start_time = time.time()
        
        # Extract outlines from all PDFs
        document_outlines = []
        for pdf_file in pdf_files:
            try:
                outline = self.pdf_processor.extract_outline(pdf_file)
                document_outlines.append({
                    "document": pdf_file,
                    "outline": outline
                })
            except Exception as e:
                print(f"Error processing {pdf_file}: {str(e)}")
                continue
        
        # Create persona embedding
        persona_embedding = self._create_persona_embedding(persona_description, job_to_be_done)
        
        # Extract and rank sections
        extracted_sections = self._extract_and_rank_sections(document_outlines, persona_embedding)
        
        # Generate sub-section analyses
        sub_section_analyses = self._generate_sub_section_analyses(extracted_sections, persona_description)
        
        # Compile results
        result = {
            "metadata": {
                "documents": pdf_files,
                "persona_description": persona_description,
                "job_to_be_done": job_to_be_done,
                "timestamp": time.time(),
                "processing_time": time.time() - start_time
            },
            "extracted_sections": extracted_sections,
            "sub_section_analyses": sub_section_analyses
        }
        
        return result
    
    def _create_persona_embedding(self, persona_description: str, job_to_be_done: str) -> np.ndarray:
        """Create embedding for persona and job-to-be-done"""
        combined_text = f"{persona_description} {job_to_be_done}"
        return self.model.encode([combined_text])[0]
    
    def _extract_and_rank_sections(self, document_outlines: List[Dict], persona_embedding: np.ndarray) -> List[Dict]:
        """Extract sections from documents and rank by relevance to persona"""
        all_sections = []
        
        for doc_outline in document_outlines:
            document = doc_outline["document"]
            outline = doc_outline["outline"]["outline"]
            
            for heading in outline:
                # Create section text (heading + context)
                section_text = heading["text"]
                
                # Create embedding for section
                section_embedding = self.model.encode([section_text])[0]
                
                # Calculate similarity to persona
                similarity = cosine_similarity([section_embedding], [persona_embedding])[0][0]
                
                # Determine importance rank based on similarity and heading level
                importance_rank = self._calculate_importance_rank(similarity, heading["level"])
                
                all_sections.append({
                    "document": document,
                    "page": heading["page"],
                    "section_title": heading["text"],
                    "importance_rank": importance_rank,
                    "similarity_score": float(similarity),
                    "level": heading["level"]
                })
        
        # Sort by importance rank (descending)
        all_sections.sort(key=lambda x: x["importance_rank"], reverse=True)
        
        return all_sections
    
    def _calculate_importance_rank(self, similarity_score: float, heading_level: str) -> float:
        """Calculate importance rank based on similarity and heading level"""
        # Base rank from similarity (0-1)
        base_rank = similarity_score
        
        # Adjust based on heading level
        level_multiplier = {
            "H1": 1.2,  # Main headings get boost
            "H2": 1.0,  # Standard weight
            "H3": 0.8   # Sub-headings get slight penalty
        }
        
        adjusted_rank = base_rank * level_multiplier.get(heading_level, 1.0)
        
        # Normalize to 0-1 range
        return min(max(adjusted_rank, 0.0), 1.0)
    
    def _generate_sub_section_analyses(self, extracted_sections: List[Dict], persona_description: str) -> List[Dict]:
        """Generate detailed analyses for top-ranked sections"""
        analyses = []
        
        # Focus on top 10 sections for detailed analysis
        top_sections = extracted_sections[:10]
        
        for section in top_sections:
            # Generate refined text based on persona
            refined_text = self._generate_refined_text(section, persona_description)
            
            analyses.append({
                "document": section["document"],
                "refined_text": refined_text,
                "page": section["page"],
                "original_title": section["section_title"],
                "relevance_explanation": self._explain_relevance(section, persona_description)
            })
        
        return analyses
    
    def _generate_refined_text(self, section: Dict, persona_description: str) -> str:
        """Generate refined text that's relevant to the persona"""
        title = section["section_title"]
        similarity = section["similarity_score"]
        
        # Create persona-focused description
        if similarity > 0.7:
            relevance_level = "highly relevant"
        elif similarity > 0.5:
            relevance_level = "moderately relevant"
        else:
            relevance_level = "somewhat relevant"
        
        refined_text = f"This section on '{title}' is {relevance_level} to your needs. "
        refined_text += f"It appears on page {section['page']} and addresses key aspects "
        refined_text += f"related to your persona and objectives."
        
        return refined_text
    
    def _explain_relevance(self, section: Dict, persona_description: str) -> str:
        """Explain why this section is relevant to the persona"""
        title = section["section_title"]
        similarity = section["similarity_score"]
        
        if similarity > 0.8:
            return f"'{title}' directly addresses your primary objectives with high relevance."
        elif similarity > 0.6:
            return f"'{title}' provides valuable context and supporting information for your goals."
        else:
            return f"'{title}' offers background information that may be useful for your research."
    
    def get_model_size(self) -> float:
        """Get approximate model size in MB"""
        # Calculate model size
        param_size = sum(p.numel() * p.element_size() for p in self.model.parameters())
        buffer_size = sum(b.numel() * b.element_size() for b in self.model.buffers())
        model_size_mb = (param_size + buffer_size) / 1024 / 1024
        return model_size_mb 