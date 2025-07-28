#!/usr/bin/env python3
"""
Adobe PDF Research Companion CLI
Command-line interface for batch PDF processing and analysis
"""

import argparse
import os
import sys
import json
import time
from pathlib import Path
from typing import List, Dict, Any

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from pdf_processor import PDFProcessor
from persona_analyzer import PersonaAnalyzer

class PDFResearchCLI:
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.persona_analyzer = PersonaAnalyzer()
    
    def extract_outline(self, pdf_path: str, output_path: str = None) -> Dict[str, Any]:
        """Extract outline from a single PDF"""
        print(f"Processing: {pdf_path}")
        start_time = time.time()
        
        try:
            result = self.pdf_processor.extract_outline(pdf_path)
            processing_time = time.time() - start_time
            
            result['processing_time'] = processing_time
            result['input_file'] = pdf_path
            
            if output_path:
                with open(output_path, 'w') as f:
                    json.dump(result, f, indent=2)
                print(f"Results saved to: {output_path}")
            
            print(f"✓ Outline extracted in {processing_time:.2f}s")
            print(f"  Title: {result['title']}")
            print(f"  Sections: {len(result['outline'])}")
            
            return result
            
        except Exception as e:
            print(f"✗ Error processing {pdf_path}: {str(e)}")
            return None
    
    def batch_extract_outlines(self, input_dir: str, output_dir: str) -> List[Dict[str, Any]]:
        """Extract outlines from all PDFs in a directory"""
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        
        if not input_path.exists():
            print(f"✗ Input directory does not exist: {input_dir}")
            return []
        
        output_path.mkdir(parents=True, exist_ok=True)
        
        pdf_files = list(input_path.glob("*.pdf"))
        if not pdf_files:
            print(f"✗ No PDF files found in: {input_dir}")
            return []
        
        print(f"Found {len(pdf_files)} PDF files")
        results = []
        
        for pdf_file in pdf_files:
            output_file = output_path / f"{pdf_file.stem}.outline.json"
            result = self.extract_outline(str(pdf_file), str(output_file))
            if result:
                results.append(result)
        
        print(f"\n✓ Processed {len(results)}/{len(pdf_files)} files successfully")
        return results
    
    def analyze_persona(self, pdf_files: List[str], persona_desc: str, job_to_be_done: str, output_path: str = None) -> Dict[str, Any]:
        """Perform persona-driven analysis on multiple PDFs"""
        print(f"Analyzing {len(pdf_files)} documents for persona: {persona_desc[:50]}...")
        start_time = time.time()
        
        try:
            result = self.persona_analyzer.analyze(pdf_files, persona_desc, job_to_be_done)
            processing_time = time.time() - start_time
            
            result['processing_time'] = processing_time
            
            if output_path:
                with open(output_path, 'w') as f:
                    json.dump(result, f, indent=2)
                print(f"Results saved to: {output_path}")
            
            print(f"✓ Analysis completed in {processing_time:.2f}s")
            print(f"  Documents analyzed: {len(result['metadata']['documents'])}")
            print(f"  Sections extracted: {len(result['extracted_sections'])}")
            print(f"  Detailed analyses: {len(result['sub_section_analyses'])}")
            
            # Show top recommendations
            print("\nTop 3 Recommended Sections:")
            for i, section in enumerate(result['extracted_sections'][:3], 1):
                print(f"  {i}. {section['section_title']} (p.{section['page']}) - Rank: {section['importance_rank']:.2f}")
            
            return result
            
        except Exception as e:
            print(f"✗ Error during persona analysis: {str(e)}")
            return None
    
    def show_model_info(self):
        """Display information about the models being used"""
        print("Model Information:")
        print(f"  PDF Processor Model: {self.pdf_processor.model_name}")
        print(f"  PDF Processor Size: {self.pdf_processor.get_model_size():.1f} MB")
        print(f"  Persona Analyzer Model: all-MiniLM-L6-v2")
        print(f"  Persona Analyzer Size: {self.persona_analyzer.get_model_size():.1f} MB")
        print(f"  Total Model Size: {self.pdf_processor.get_model_size() + self.persona_analyzer.get_model_size():.1f} MB")

def main():
    parser = argparse.ArgumentParser(
        description="Adobe PDF Research Companion CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract outline from a single PDF
  python cli.py outline document.pdf -o result.json
  
  # Batch process all PDFs in a directory
  python cli.py batch input/ output/
  
  # Persona analysis
  python cli.py persona docs/ "Data Scientist" "Implement ML pipeline" -o analysis.json
  
  # Show model information
  python cli.py info
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Outline extraction command
    outline_parser = subparsers.add_parser('outline', help='Extract outline from a single PDF')
    outline_parser.add_argument('pdf_file', help='Path to PDF file')
    outline_parser.add_argument('-o', '--output', help='Output JSON file path')
    
    # Batch processing command
    batch_parser = subparsers.add_parser('batch', help='Batch process PDFs in a directory')
    batch_parser.add_argument('input_dir', help='Input directory containing PDFs')
    batch_parser.add_argument('output_dir', help='Output directory for results')
    
    # Persona analysis command
    persona_parser = subparsers.add_parser('persona', help='Perform persona-driven analysis')
    persona_parser.add_argument('input_dir', help='Directory containing PDF files')
    persona_parser.add_argument('persona', help='Persona description')
    persona_parser.add_argument('job', help='Job to be done')
    persona_parser.add_argument('-o', '--output', help='Output JSON file path')
    
    # Model info command
    subparsers.add_parser('info', help='Show model information')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = PDFResearchCLI()
    
    if args.command == 'outline':
        cli.extract_outline(args.pdf_file, args.output)
    
    elif args.command == 'batch':
        cli.batch_extract_outlines(args.input_dir, args.output_dir)
    
    elif args.command == 'persona':
        input_path = Path(args.input_dir)
        pdf_files = [str(f) for f in input_path.glob("*.pdf")]
        
        if len(pdf_files) < 3:
            print("✗ Persona analysis requires at least 3 PDF files")
            return
        
        if len(pdf_files) > 10:
            print("✗ Persona analysis supports maximum 10 PDF files")
            return
        
        cli.analyze_persona(pdf_files, args.persona, args.job, args.output)
    
    elif args.command == 'info':
        cli.show_model_info()

if __name__ == "__main__":
    main() 