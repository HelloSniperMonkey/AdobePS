from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import json
import time
from typing import List, Optional
from pydantic import BaseModel

from pdf_processor import PDFProcessor
from persona_analyzer import PersonaAnalyzer

app = FastAPI(
    title="Adobe PDF Research Companion API",
    description="Intelligent PDF analysis and persona-driven insights",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize processors
pdf_processor = PDFProcessor()
persona_analyzer = PersonaAnalyzer()

class PersonaRequest(BaseModel):
    persona_description: str
    job_to_be_done: str
    pdf_files: List[str]  # List of PDF file paths

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/extract-outline")
async def extract_outline(file: UploadFile = File(...)):
    """
    Round 1A: Extract PDF outline
    Input: Single PDF file (≤50 pages)
    Output: JSON with title and hierarchical outline
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="File must be a PDF")
        
        # Save uploaded file temporarily
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process PDF
        start_time = time.time()
        result = pdf_processor.extract_outline(temp_path)
        processing_time = time.time() - start_time
        
        # Clean up
        os.remove(temp_path)
        
        return {
            "success": True,
            "processing_time": processing_time,
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-persona")
async def analyze_persona(request: PersonaRequest):
    """
    Round 1B: Persona-driven analysis
    Input: 3-10 related PDFs + persona description + job-to-be-done
    Output: JSON with metadata, extracted sections, and analyses
    """
    try:
        # Validate number of PDFs
        if len(request.pdf_files) < 3 or len(request.pdf_files) > 10:
            raise HTTPException(
                status_code=400, 
                detail="Number of PDF files must be between 3 and 10"
            )
        
        # Process persona analysis
        start_time = time.time()
        result = persona_analyzer.analyze(
            pdf_files=request.pdf_files,
            persona_description=request.persona_description,
            job_to_be_done=request.job_to_be_done
        )
        processing_time = time.time() - start_time
        
        return {
            "success": True,
            "processing_time": processing_time,
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch-process")
async def batch_process(background_tasks: BackgroundTasks):
    """
    Batch processing endpoint for Docker container
    Processes all PDFs in /app/input and saves results to /app/output
    """
    def process_batch():
        input_dir = "/app/input"
        output_dir = "/app/output"
        
        if not os.path.exists(input_dir):
            os.makedirs(input_dir)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(input_dir, pdf_file)
            try:
                # Extract outline
                outline_result = pdf_processor.extract_outline(pdf_path)
                
                # Save result
                output_file = os.path.join(output_dir, f"{pdf_file}.outline.json")
                with open(output_file, 'w') as f:
                    json.dump(outline_result, f, indent=2)
                    
            except Exception as e:
                print(f"Error processing {pdf_file}: {str(e)}")
    
    background_tasks.add_task(process_batch)
    return {"message": "Batch processing started"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 