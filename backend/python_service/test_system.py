#!/usr/bin/env python3
"""
NPL System Verification Script
Tests Ollama integration and file handling capabilities
"""

import requests
import json
import sys
from pathlib import Path

# Configuration
BACKEND_URL = "http://localhost:3000"
PYTHON_SERVICE_URL = "http://localhost:5000"
OLLAMA_URL = "http://localhost:11434"

def print_status(message, status="info"):
    """Print formatted status message"""
    icons = {
        "ok": "✓",
        "error": "✗",
        "warning": "⚠",
        "info": "ℹ"
    }
    colors = {
        "ok": "\033[92m",
        "error": "\033[91m",
        "warning": "\033[93m",
        "info": "\033[94m",
        "reset": "\033[0m"
    }
    icon = icons.get(status, "•")
    color = colors.get(status, colors["reset"])
    print(f"{color}{icon} {message}{colors['reset']}")

def test_ollama():
    """Test Ollama connectivity"""
    print("\n--- Testing Ollama ---")
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            if models:
                print_status("Ollama is running", "ok")
                print(f"  Found {len(models)} model(s):")
                for model in models:
                    model_name = model.get("name", "unknown")
                    print(f"    - {model_name}")
                return True
            else:
                print_status("Ollama is running but no models found", "warning")
                print("  Install a model: ollama pull llama2")
                return False
        else:
            print_status(f"Ollama returned status {response.status_code}", "error")
            return False
    except requests.exceptions.ConnectionError:
        print_status(f"Cannot connect to Ollama at {OLLAMA_URL}", "error")
        print("  Make sure Ollama is running: ollama serve")
        return False
    except Exception as e:
        print_status(f"Ollama test failed: {e}", "error")
        return False

def test_python_service():
    """Test Python NLP service"""
    print("\n--- Testing Python NLP Service ---")
    try:
        response = requests.get(f"{PYTHON_SERVICE_URL}/health", timeout=3)
        if response.status_code == 200:
            data = response.json()
            print_status("Python service is running", "ok")
            print(f"  Status: {data.get('status')}")
            print(f"  NLP loaded: {data.get('nlp_loaded')}")
            print(f"  Ollama available: {data.get('ollama_available')}")
            print(f"  Model: {data.get('ollama_model')}")
            print(f"  Supported formats: {', '.join(data.get('supported_formats', []))}")
            return True
        else:
            print_status(f"Service returned status {response.status_code}", "error")
            return False
    except requests.exceptions.ConnectionError:
        print_status(f"Cannot connect to Python service at {PYTHON_SERVICE_URL}", "error")
        print("  Start Python service: uvicorn app:app --port 5000")
        return False
    except Exception as e:
        print_status(f"Service test failed: {e}", "error")
        return False

def test_backend():
    """Test Node backend"""
    print("\n--- Testing Node Backend ---")
    try:
        response = requests.get(BACKEND_URL, timeout=3)
        if response.status_code == 200:
            print_status("Backend is running", "ok")
            return True
        else:
            print_status(f"Backend returned status {response.status_code}", "error")
            return False
    except requests.exceptions.ConnectionError:
        print_status(f"Cannot connect to backend at {BACKEND_URL}", "error")
        print("  Start backend: npm run dev")
        return False
    except Exception as e:
        print_status(f"Backend test failed: {e}", "error")
        return False

def test_general_qa():
    """Test general Q&A without document"""
    print("\n--- Testing General Q&A ---")
    try:
        payload = {
            "text": "",
            "question": "What is artificial intelligence?",
            "features": {
                "answer": True
            }
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/analyze",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("answer"):
                print_status("General Q&A working", "ok")
                print(f"  Question: {payload['question'][:50]}...")
                print(f"  Answer: {data['answer'][:100]}...")
                print(f"  Source: {data.get('source', 'unknown')}")
                print(f"  Model: {data.get('model', 'unknown')}")
                print(f"  Confidence: {data.get('confidence', 'N/A')}")
                return True
            else:
                print_status("No answer received", "warning")
                return False
        else:
            print_status(f"Request failed with status {response.status_code}", "error")
            print(f"  Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print_status("Request timeout - Ollama might be slow", "warning")
        return False
    except Exception as e:
        print_status(f"General Q&A test failed: {e}", "error")
        return False

def test_text_qa():
    """Test Q&A with document text"""
    print("\n--- Testing Document Q&A ---")
    try:
        payload = {
            "text": "Machine Learning is a subset of Artificial Intelligence. It enables computers to learn from data without being explicitly programmed.",
            "question": "What is Machine Learning?",
            "features": {
                "answer": True,
                "entities": True
            }
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/analyze",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("answer"):
                print_status("Document Q&A working", "ok")
                print(f"  Question: {payload['question']}")
                print(f"  Answer: {data['answer'][:100]}...")
                print(f"  Entities found: {len(data.get('entities', []))}")
                return True
            else:
                print_status("No answer received", "warning")
                return False
        else:
            print_status(f"Request failed with status {response.status_code}", "error")
            return False
            
    except requests.exceptions.Timeout:
        print_status("Request timeout", "warning")
        return False
    except Exception as e:
        print_status(f"Document Q&A test failed: {e}", "error")
        return False

def create_test_files():
    """Create sample test files"""
    print("\n--- Creating Test Files ---")
    
    test_dir = Path("test_uploads")
    test_dir.mkdir(exist_ok=True)
    
    # Create test TXT file
    txt_file = test_dir / "sample.txt"
    txt_file.write_text("""
    Natural Language Processing (NLP) is a subfield of linguistics, computer science,
    and artificial intelligence concerned with the interactions between computers and human language.
    
    NLP is used to apply machine learning algorithms to text and speech.
    """)
    print_status(f"Created test file: {txt_file}", "ok")
    
    # Instructions for PDF and DOCX
    print_status("To test PDF and DOCX uploads:", "info")
    print("  - Create a PDF file and place it in test_uploads/ directory")
    print("  - Create a DOCX file and place it in test_uploads/ directory")
    print("  - Use this script to upload and test")

def main():
    """Run all tests"""
    print("=" * 60)
    print("NPL System Verification")
    print("=" * 60)
    
    results = {
        "Ollama": test_ollama(),
        "Python Service": test_python_service(),
        "Backend": test_backend(),
        "General Q&A": test_general_qa(),
        "Document Q&A": test_text_qa(),
    }
    
    create_test_files()
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for service, passed in results.items():
        status = "ok" if passed else "error"
        print_status(f"{service}: {'PASS' if passed else 'FAIL'}", status)
    
    total_passed = sum(1 for v in results.values() if v)
    total_tests = len(results)
    
    print("\n" + "=" * 60)
    if total_passed == total_tests:
        print_status(f"All tests passed ({total_passed}/{total_tests})!", "ok")
        print("\nYour system is ready to use! Try uploading a document and asking questions.")
    else:
        print_status(f"Some tests failed ({total_passed}/{total_tests})", "warning")
        print("\nFix the issues above and try again.")
    print("=" * 60)

if __name__ == "__main__":
    main()
