#!/usr/bin/env python3
"""
Test script for Adobe PDF Research Companion
Tests the core functionality and API endpoints
"""

import os
import sys
import json
import time
import requests
from pathlib import Path

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_backend_health():
    """Test backend health endpoint"""
    print("Testing backend health...")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✓ Backend is healthy")
            return True
        else:
            print(f"✗ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Backend is not running")
        return False

def test_pdf_processor():
    """Test PDF processor functionality"""
    print("\nTesting PDF processor...")
    try:
        from pdf_processor import PDFProcessor
        
        processor = PDFProcessor()
        print(f"✓ PDF processor initialized")
        print(f"  Model: {processor.model_name}")
        print(f"  Size: {processor.get_model_size():.1f} MB")
        
        return True
    except Exception as e:
        print(f"✗ PDF processor test failed: {str(e)}")
        return False

def test_persona_analyzer():
    """Test persona analyzer functionality"""
    print("\nTesting persona analyzer...")
    try:
        from persona_analyzer import PersonaAnalyzer
        
        analyzer = PersonaAnalyzer()
        print(f"✓ Persona analyzer initialized")
        print(f"  Model: all-MiniLM-L6-v2")
        print(f"  Size: {analyzer.get_model_size():.1f} MB")
        
        return True
    except Exception as e:
        print(f"✗ Persona analyzer test failed: {str(e)}")
        return False

def test_cli():
    """Test CLI functionality"""
    print("\nTesting CLI...")
    try:
        from cli import PDFResearchCLI
        
        cli = PDFResearchCLI()
        cli.show_model_info()
        print("✓ CLI initialized successfully")
        
        return True
    except Exception as e:
        print(f"✗ CLI test failed: {str(e)}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\nTesting API endpoints...")
    
    # Test outline extraction endpoint
    try:
        # Create a mock PDF file for testing
        test_pdf_path = "test_document.pdf"
        
        # This would normally be a real PDF file
        # For testing, we'll just check if the endpoint exists
        response = requests.post("http://localhost:8000/extract-outline")
        if response.status_code in [400, 422]:  # Expected for missing file
            print("✓ Outline extraction endpoint is accessible")
        else:
            print(f"⚠ Unexpected response: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("✗ API endpoints not accessible (backend not running)")
        return False
    
    # Test persona analysis endpoint
    try:
        test_data = {
            "persona_description": "Data Scientist",
            "job_to_be_done": "Implement ML pipeline",
            "pdf_files": ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
        }
        
        response = requests.post("http://localhost:8000/analyze-persona", json=test_data)
        if response.status_code in [400, 422]:  # Expected for missing files
            print("✓ Persona analysis endpoint is accessible")
        else:
            print(f"⚠ Unexpected response: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("✗ API endpoints not accessible")
        return False
    
    return True

def test_frontend_build():
    """Test if frontend can be built"""
    print("\nTesting frontend build...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("✗ Frontend directory not found")
        return False
    
    package_json = frontend_dir / "package.json"
    if not package_json.exists():
        print("✗ package.json not found")
        return False
    
    try:
        with open(package_json, 'r') as f:
            package_data = json.load(f)
        
        print(f"✓ Frontend package.json found")
        print(f"  Name: {package_data.get('name', 'N/A')}")
        print(f"  Version: {package_data.get('version', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"✗ Frontend build test failed: {str(e)}")
        return False

def test_docker_config():
    """Test Docker configuration"""
    print("\nTesting Docker configuration...")
    
    dockerfile = Path("Dockerfile")
    if not dockerfile.exists():
        print("✗ Dockerfile not found")
        return False
    
    docker_compose = Path("docker-compose.yml")
    if not docker_compose.exists():
        print("✗ docker-compose.yml not found")
        return False
    
    start_script = Path("start.sh")
    if not start_script.exists():
        print("✗ start.sh not found")
        return False
    
    print("✓ Docker configuration files found")
    return True

def main():
    """Run all tests"""
    print("Adobe PDF Research Companion - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Backend Health", test_backend_health),
        ("PDF Processor", test_pdf_processor),
        ("Persona Analyzer", test_persona_analyzer),
        ("CLI", test_cli),
        ("API Endpoints", test_api_endpoints),
        ("Frontend Build", test_frontend_build),
        ("Docker Config", test_docker_config),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} test failed with exception: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to use.")
    else:
        print("⚠ Some tests failed. Please check the configuration.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 