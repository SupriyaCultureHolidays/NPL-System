#!/usr/bin/env python3
"""
Diagnostic script to identify issues and test all components
"""

import requests
import json
import sys

# Configuration
BACKEND_URL = "http://localhost:3000"
PYTHON_SERVICE_URL = "http://localhost:5000"
OLLAMA_URL = "http://localhost:11434"

def print_test(name, result, details=""):
    """Print test result"""
    icon = "✅" if result else "❌"
    print(f"{icon} {name}")
    if details:
        print(f"   {details}")

def test_backend():
    """Test if backend is running"""
    print("\n=== Backend Test ===")
    try:
        resp = requests.get(f"{BACKEND_URL}/health", timeout=3)
        if resp.status_code == 200:
            print_test("Backend is running", True)
            data = resp.json()
            print(f"   Status: {data.get('status')}")
            return True
        else:
            print_test("Backend responded but with error", False, f"Status: {resp.status_code}")
            return False
    except Exception as e:
        print_test("Backend is NOT running", False, f"Error: {e}")
        return False

def test_python_service():
    """Test if Python service is running"""
    print("\n=== Python Service Test ===")
    try:
        resp = requests.get(f"{PYTHON_SERVICE_URL}/health", timeout=3)
        if resp.status_code == 200:
            print_test("Python service is running", True)
            data = resp.json()
            print(f"   NLP loaded: {data.get('nlp_loaded')}")
            print(f"   Ollama available: {data.get('ollama_available')}")
            print(f"   Model: {data.get('ollama_model')}")
            return data.get('ollama_available')
        else:
            print_test("Python service responded with error", False, f"Status: {resp.status_code}")
            return False
    except Exception as e:
        print_test("Python service is NOT running", False, f"Error: {e}")
        return False

def test_ollama():
    """Test if Ollama is running"""
    print("\n=== Ollama Test ===")
    try:
        resp = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            models = data.get('models', [])
            if models:
                print_test("Ollama is running", True)
                print(f"   Models installed: {len(models)}")
                for model in models:
                    print(f"      - {model.get('name')}")
                return True
            else:
                print_test("Ollama running but no models found", False)
                print("   Run: ollama pull llama2")
                return False
        else:
            print_test(f"Ollama returned status {resp.status_code}", False)
            return False
    except Exception as e:
        print_test("Ollama is NOT running", False, f"Error: {e}")
        print(f"   Start with: ollama serve")
        return False

def test_ollama_directly():
    """Test Ollama LLM directly"""
    print("\n=== Direct Ollama LLM Test ===")
    try:
        resp = requests.post(
            f"{PYTHON_SERVICE_URL}/test-ollama",
            params={"question": "What is 2+2?"},
            timeout=60
        )
        data = resp.json()
        if data.get('status') == 'success':
            print_test("Ollama LLM responded", True)
            print(f"   Question: {data.get('question')}")
            print(f"   Answer: {data.get('answer')[:100]}...")
            print(f"   Model: {data.get('model')}")
            return True
        else:
            print_test("Ollama LLM failed", False)
            print(f"   Error: {data.get('error')}")
            print(f"   Suggestion: {data.get('suggestion')}")
            return False
    except requests.exceptions.Timeout:
        print_test("Ollama LLM timed out", False)
        print("   Increase OLLAMA_TIMEOUT or check system resources")
        return False
    except Exception as e:
        print_test("Ollama LLM test failed", False, f"Error: {e}")
        return False

def test_general_qa():
    """Test general Q&A through backend"""
    print("\n=== Backend General Q&A Test ===")
    try:
        payload = {
            "question": "Who is the current prime minister of India?",
            "features": {"answer": True}
        }
        resp = requests.post(
            f"{BACKEND_URL}/api/analyze",
            json=payload,
            timeout=60
        )
        
        if resp.status_code == 200:
            data = resp.json()
            if 'answer' in data and data['answer']:
                print_test("Got answer from backend", True)
                print(f"   Question: {payload['question']}")
                print(f"   Answer: {data['answer'][:100]}...")
                print(f"   Source: {data.get('source', 'unknown')}")
                return True
            else:
                print_test("No answer in response", False)
                print(f"   Response: {json.dumps(data, indent=2)[:200]}")
                return False
        else:
            print_test(f"Backend returned status {resp.status_code}", False)
            print(f"   Response: {resp.text[:200]}")
            return False
    except requests.exceptions.Timeout:
        print_test("Request timed out", False)
        return False
    except Exception as e:
        print_test("General Q&A test failed", False, f"Error: {e}")
        return False

def test_file_upload():
    """Test file upload"""
    print("\n=== File Upload Test ===")
    try:
        # Create a test text file
        with open('/tmp/test.txt', 'w') as f:
            f.write("India is a country in South Asia. The current Prime Minister of India is Narendra Modi.")
        
        with open('/tmp/test.txt', 'rb') as f:
            files = {'file': f}
            data = {'question': 'Who is the PM of India?'}
            
            resp = requests.post(
                f"{BACKEND_URL}/api/analyze",
                files=files,
                data=data,
                timeout=60
            )
        
        if resp.status_code == 200:
            result = resp.json()
            if 'answer' in result and result['answer']:
                print_test("File upload and Q&A working", True)
                print(f"   Answer: {result['answer'][:100]}...")
                return True
            else:
                print_test("No answer from file Q&A", False)
                return False
        else:
            print_test(f"Upload returned status {resp.status_code}", False)
            return False
    except Exception as e:
        print_test("File upload test failed", False, f"Error: {e}")
        return False

def main():
    """Run all diagnostics"""
    print("=" * 60)
    print("NPL System Diagnostic Test")
    print("=" * 60)
    
    results = {}
    
    # Test each component
    results['backend'] = test_backend()
    results['python'] = test_python_service()
    results['ollama'] = test_ollama()
    
    if results['python'] and results['ollama']:
        results['ollama_llm'] = test_ollama_directly()
    
    if results['backend']:
        results['general_qa'] = test_general_qa()
        results['file_upload'] = test_file_upload()
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test}")
    
    # Recommendations
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS")
    print("=" * 60)
    
    if not results.get('backend'):
        print("❌ Start backend: cd backend && npm run dev")
    
    if not results.get('python'):
        print("❌ Start Python service: cd backend/python_service && python -m uvicorn app:app --port 5000")
    
    if not results.get('ollama'):
        print("❌ Start Ollama: ollama serve")
        print("❌ Install model: ollama pull llama2")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed! System should be working.")
        print("\nIf you're still not seeing answers in frontend:")
        print("1. Check browser console (F12 → Console tab)")
        print("2. Check backend terminal for logs")
        print("3. Refresh the page")
    else:
        print("❌ Some tests failed. Fix the issues above and try again.")
    print("=" * 60)

if __name__ == "__main__":
    main()
