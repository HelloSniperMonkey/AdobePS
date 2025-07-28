# Adobe PDF Research Companion

An intelligent, interactive research companion that transforms static PDF libraries into dynamic, persona-driven knowledge systems.

## Project Vision

Turn a static PDF library into an intelligent, interactive research companion that extracts structure, surfaces insights, and personalizes document views based on user personas and job-to-be-done scenarios.

## Core Functionality

### Round 1A – PDF Outline Extractor
- **Input**: Single PDF (≤50 pages)
- **Output**: JSON with title and hierarchical outline
- **Constraints**: Offline, CPU-only, ≤200MB model, ≤10s runtime

### Round 1B – Persona-Driven Intelligence
- **Input**: 3-10 related PDFs + persona description + job-to-be-done
- **Output**: JSON with metadata, extracted sections, and sub-section analyses
- **Constraints**: Offline, CPU-only, ≤1GB model, ≤60s runtime

### Round 2 – Interactive Web App
- Adobe PDF Embed API integration
- Collapsible outline panel
- Persona-focused recommended sections
- On-demand detail drill-downs

## Quick Start

### Prerequisites
- Docker
- Node.js 18+ (for development)
- Python 3.9+ (for development)

### Build and Run

1. **Build the Docker image:**
```bash
docker build -t adobe-pdf-research .
```

2. **Run the application:**
```bash
docker run -p 8000:8000 -p 3000:3000 adobe-pdf-research
```

3. **Access the application:**
- Web UI: http://localhost:3000
- API Docs: http://localhost:8000/docs

### Batch Processing

For batch PDF processing:
```bash
docker run -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output adobe-pdf-research
```

## Development Setup

### Backend (Python + FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (React)
```bash
cd frontend
npm install
npm start
```

## API Endpoints

- `POST /extract-outline` - Extract PDF outline (Round 1A)
- `POST /analyze-persona` - Persona-driven analysis (Round 1B)
- `GET /health` - Health check

## Architecture

- **Backend**: Python + FastAPI + PyPDF2 + sentence-transformers
- **Frontend**: React + Adobe PDF Embed API
- **Models**: Lightweight transformers for heading detection and semantic analysis
- **Containerization**: Single Docker image with all dependencies

## License

Private repository until go-public notice. 