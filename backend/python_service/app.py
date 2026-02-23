from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from pydantic import BaseModel
import spacy
import pdfplumber
import json
import os
import logging
from typing import Optional, Dict, Any, List, Tuple
import requests
from docx import Document

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.error("Spacy model not found. Install with: python -m spacy download en_core_web_sm")
    nlp = None

# Configuration from environment
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "30"))

app = FastAPI(title="Python NLP Service")

class TextRequest(BaseModel):
    text: str

def _extract_text_from_docx(file_obj) -> str:
    """Extract text from DOCX file"""
    try:
        doc = Document(file_obj)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        logger.error(f"DOCX extraction error: {e}")
        return ""

def _extract_text_from_pdf(file_obj) -> str:
    """Extract text from PDF file"""
    try:
        with pdfplumber.open(file_obj) as pdf:
            return "".join([p.extract_text() or "" for p in pdf.pages])
    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        return ""

def _extract_text_from_upload(file: UploadFile) -> str:
    """Extract text from uploaded file (PDF, DOCX, TXT)"""
    name = (file.filename or "").lower()
    
    # PDF handling
    if name.endswith(".pdf") or (file.content_type or "") == "application/pdf":
        return _extract_text_from_pdf(file.file)
    
    # DOCX handling
    if name.endswith(".docx") or (file.content_type or "") == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return _extract_text_from_docx(file.file)
    
    # Plain text handling (default)
    try:
        return file.file.read().decode("utf-8", errors="ignore")
    except Exception as e:
        logger.error(f"Text extraction error: {e}")
        return ""

def _collect_entities(doc) -> Dict[str, List[str]]:
    by_label: Dict[str, List[str]] = {}
    for ent in doc.ents:
        by_label.setdefault(ent.label_, []).append(ent.text)
    return by_label

def _wh_answer(doc, question: str) -> Optional[Tuple[str, float]]:
    ql = question.lower()
    ents = _collect_entities(doc)
    if "who" in ql:
        c = ents.get("PERSON", [])
        if c:
            return (max(set(c), key=c.count), 0.9)
    if "where" in ql:
        c = (ents.get("GPE", []) + ents.get("LOC", []) + ents.get("FAC", []))
        if c:
            return (max(set(c), key=c.count), 0.85)
    if "when" in ql:
        c = (ents.get("DATE", []) + ents.get("TIME", []))
        if c:
            return (max(set(c), key=c.count), 0.85)
    return None

def _overlap_answer(doc, question: str) -> Tuple[str, float, List[Tuple[str, float]]]:
    q = nlp(question)
    qset = {t.lemma_.lower() for t in q if not t.is_stop and not t.is_punct}
    scores: List[Tuple[str, float]] = []
    for s in doc.sents:
        sset = {t.lemma_.lower() for t in s if not t.is_stop and not t.is_punct}
        overlap = len(qset & sset)
        denom = len(qset) or 1
        score = overlap / denom
        scores.append((s.text, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    best_sent, best_score = (scores[0] if scores else ("", 0.0))
    return best_sent.strip(), round(best_score, 3), scores[:3]

def _answer_from_text(text: str, question: str) -> Dict[str, Any]:
    if not nlp:
        return {"answer": "", "confidence": 0.0, "evidence": []}
    
    d = nlp(text)
    if len([t for t in d if not t.is_space]) < 3:
        return {"answer": "", "confidence": 0.0, "evidence": []}
    
    wh = _wh_answer(d, question)
    if wh:
        ans, conf = wh
        return {"answer": ans, "confidence": conf, "evidence": []}
    
    ans, conf, evid = _overlap_answer(d, question)
    if conf < 0.2 or ans.strip().lower() == question.strip().lower():
        return {"answer": "", "confidence": conf, "evidence": evid}
    
    return {"answer": ans, "confidence": conf, "evidence": evid}

def _check_ollama_available() -> bool:
    """Check if Ollama is available"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=2)
        return response.status_code == 200
    except Exception as e:
        logger.warning(f"Ollama not available: {e}")
        return False

def _call_ollama_llm(document_text: str, question: str, use_context: bool = True) -> Optional[Dict[str, Any]]:
    """Call Ollama LLM with improved prompt and error handling"""
    
    # Build context-aware prompt
    if use_context and document_text.strip():
        prompt = f"""You are an intelligent AI assistant analyzing a document.

INSTRUCTIONS:
1. If the answer can be found in the provided DOCUMENT CONTEXT, use that information.
2. If the answer is NOT in the document, use your general knowledge to answer.
3. Provide a clear, accurate answer.
4. Do not say whether the answer came from the document or your knowledge.
5. Be concise and direct.
6. Public factual questions about public figures (e.g., age) are allowed and should be answered. Do not refuse them. If you genuinely do not know, say you don't know.

DOCUMENT:
{document_text[:2000]}  [Truncated for performance]

QUESTION: {question}

ANSWER:"""
    else:
        prompt = f"""You are a helpful AI assistant.

QUESTION: {question}

Please provide a clear and accurate answer. Public factual questions about public figures (e.g., age) are allowed and should be answered. Do not refuse them. If you genuinely do not know, say you don't know."""
    
    try:
        logger.info(f"Calling Ollama with model: {OLLAMA_MODEL}")
        
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.2,
            },
            timeout=OLLAMA_TIMEOUT,
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get("response", "").strip()
            
            return {
                "answer": answer,
                "source": "ollama",
                "model": OLLAMA_MODEL,
                "confidence": 0.95
            }
        else:
            logger.error(f"Ollama error: {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        logger.error("Ollama request timeout")
        return None
    except requests.exceptions.ConnectionError:
        logger.error(f"Cannot connect to Ollama at {OLLAMA_BASE_URL}")
        return None
    except Exception as e:
        logger.error(f"Ollama call error: {e}")
        return None

@app.post("/analyze")
async def analyze(
    request: Request,
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    question: Optional[str] = Form(None),
    features: Optional[str] = Form(None),
):
    """
    Analyze text/document with optional Q&A using Ollama.
    
    Supports:
    - PDF files
    - DOCX files  
    - TXT files
    - Plain text
    - Questions with or without document context
    """
    
    data = None
    ct = request.headers.get("content-type", "")
    
    # Parse JSON if content is JSON
    if "application/json" in ct:
        data = await request.json()
        text = data.get("text")
        question = data.get("question")
        features = data.get("features")
    
    logger.info(f"=== ANALYZE REQUEST ===")
    logger.info(f"Has text: {bool(text)}, Has question: {bool(question)}, Has file: {bool(file)}")
    
    # Extract text from uploaded file
    if file:
        logger.info(f"📄 Processing uploaded file: {file.filename}")
        text = _extract_text_from_upload(file)
        logger.info(f"✓ Extracted text length: {len(text)}")
    
    # Validate input
    if not text and not question:
        raise HTTPException(status_code=400, detail="Text, file, or question is required")

    result: Dict[str, Any] = {}
    
    # Parse feature flags early
    feats_dict = None
    if features:
        try:
            feats_dict = features if isinstance(features, dict) else json.loads(features)
        except Exception:
            feats_dict = None
    want_tokens = (not feats_dict) or bool(feats_dict.get("tokens"))
    want_pos = (not feats_dict) or bool(feats_dict.get("pos"))
    want_entities = (not feats_dict) or bool(feats_dict.get("entities"))
    want_lemmas = (not feats_dict) or bool(feats_dict.get("lemmas"))
    want_deps = (not feats_dict) or bool(feats_dict.get("dependencies"))
    want_confidence = bool(feats_dict.get("confidence")) if isinstance(feats_dict, dict) else False
    want_source = bool(feats_dict.get("source")) if isinstance(feats_dict, dict) else False
    want_evidence = bool(feats_dict.get("evidence")) if isinstance(feats_dict, dict) else False

    # NLP analysis if text is provided
    if text and nlp:
        logger.info("🔍 Running NLP analysis")
        doc = nlp(text)
        if want_tokens:
            result["tokens"] = [token.text for token in doc]
        if want_pos:
            result["pos"] = [{token.text: token.pos_} for token in doc]
        if want_entities:
            result["entities"] = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
        if want_lemmas:
            result["lemmas"] = [{token.text: token.lemma_} for token in doc]
        if want_deps:
            result["dependencies"] = [
                {"token": token.text, "dep": token.dep_, "head": token.head.text}
                for token in doc
            ]
        logger.info(f"✓ Found {len(doc.ents)} entities")

    # Q&A handling
    if question:
        logger.info(f"❓ Processing question: {question}")
        
        # Determine if context is relevant to question
        use_context = False
        context_text = ""
        
        if text and nlp:
            logger.info("🔗 Checking if question relates to document...")
            # Check keyword overlap between question and context
            q_doc = nlp(question)
            q_lemmas = {t.lemma_.lower() for t in q_doc if not t.is_stop and not t.is_punct}
            text_lemmas = {t.lemma_.lower() for t in nlp(text) if not t.is_stop and not t.is_punct}
            
            overlap = len(q_lemmas & text_lemmas)
            if overlap > 0:
                logger.info(f"✓ Found {overlap} keyword overlaps - using document context")
                use_context = True
                context_text = text[:2000]
            else:
                logger.info("✗ No keyword overlap - using general knowledge mode")
        else:
            logger.info("💡 No text provided - using general knowledge mode")

        # Check if Ollama is available
        ollama_available = _check_ollama_available()
        logger.info(f"Ollama available: {ollama_available}")
        
        # Try Ollama first
        if ollama_available:
            logger.info(f"🤖 Calling Ollama with model: {OLLAMA_MODEL}")
            llm_result = _call_ollama_llm(context_text, question, use_context)
            if llm_result:
                result["answer"] = llm_result["answer"]
                if want_source:
                    result["source"] = llm_result["source"]
                    result["model"] = llm_result["model"]
                if want_confidence:
                    result["confidence"] = llm_result["confidence"]
                logger.info(f"✅ Got answer from Ollama ({len(llm_result['answer'])} chars)")
                
                # Apply feature filter if requested
                if feats_dict:
                    try:
                        filtered = {}
                        for k, v in feats_dict.items():
                            if v and k in result:
                                filtered[k] = result[k]
                        filtered["answer"] = result.get("answer")
                        if feats_dict.get("source"):
                            filtered["source"] = result.get("source")
                            filtered["model"] = result.get("model")
                        if feats_dict.get("confidence"):
                            filtered["confidence"] = result.get("confidence")
                        logger.info(f"✓ Applied feature filter")
                        return filtered
                    except Exception as e:
                        logger.error(f"Feature filtering error: {e}")
                
                return result
            else:
                logger.warning("❌ Ollama returned no answer, trying fallback")
        else:
            logger.warning("⚠️ Ollama not available, falling back to pattern matching")
        
        # Fallback to spacy-based Q&A
        if text and nlp:
            logger.info("📊 Using spacy-based question answering")
            qa = _answer_from_text(text, question)
            result["answer"] = qa["answer"]
            if want_confidence:
                result["confidence"] = qa["confidence"]
            if want_evidence:
                result["evidence"] = [{"text": s, "score": sc} for s, sc in qa.get("evidence", [])]
            if want_source:
                result["source"] = "spacy"
            logger.info(f"✓ Spacy answer: '{qa['answer'][:50]}...'")
        else:
            logger.warning("❌ No text and no Ollama - cannot answer")
            result["answer"] = "No answer available. Please provide text or ensure Ollama is running."
            result["source"] = "error"
            result["confidence"] = 0.0
    
    # Apply feature filter if Q&A wasn't handled above
    if features and "answer" not in result:
        try:
            feats = features if isinstance(features, dict) else json.loads(features)
            if isinstance(feats, dict):
                filtered = {}
                for k, v in feats.items():
                    if v and k in result:
                        filtered[k] = result[k]
                logger.info(f"✓ Applied feature filter to NLP results")
                return filtered
        except Exception as e:
            logger.error(f"Feature filtering error: {e}")
    
    logger.info(f"✅ Returning result with {len(result)} keys")
    return result

@app.post("/api/analyze")
async def analyze_api(
    request: Request,
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    question: Optional[str] = Form(None),
    features: Optional[str] = Form(None),
):
    """Alternative endpoint path for /api/analyze"""
    return await analyze(request, file, text, question, features)

@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "NLP Service",
        "ollama_available": _check_ollama_available(),
        "ollama_model": OLLAMA_MODEL,
        "ollama_url": OLLAMA_BASE_URL
    }

@app.get("/health")
def health():
    """Detailed health check"""
    return {
        "status": "ok",
        "nlp_loaded": nlp is not None,
        "ollama_available": _check_ollama_available(),
        "ollama_model": OLLAMA_MODEL,
        "ollama_url": OLLAMA_BASE_URL,
        "supported_formats": [".pdf", ".docx", ".txt"],
    }

@app.post("/test-ollama")
async def test_ollama(question: str = "What is the capital of India?"):
    """Simple test endpoint - directly get Ollama response"""
    logger.info(f"🧪 Testing Ollama with question: {question}")
    
    if not _check_ollama_available():
        return {
            "error": "Ollama is not running",
            "status": "failed",
            "ollama_url": OLLAMA_BASE_URL,
            "suggestion": f"Start Ollama with: ollama serve"
        }
    
    prompt = f"""You are a helpful AI assistant.

QUESTION: {question}

Please provide a clear and accurate answer."""
    
    try:
        logger.info(f"🤖 Calling Ollama at {OLLAMA_BASE_URL}/api/generate with model {OLLAMA_MODEL}")
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7,
            },
            timeout=OLLAMA_TIMEOUT,
        )
        
        logger.info(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get("response", "").strip()
            logger.info(f"✅ Got answer: {answer[:100]}...")
            return {
                "status": "success",
                "question": question,
                "answer": answer,
                "model": OLLAMA_MODEL,
                "ollama_available": True
            }
        else:
            logger.error(f"Ollama returned status {response.status_code}")
            return {
                "status": "failed",
                "error": f"Ollama returned status {response.status_code}",
                "response_text": response.text[:200]
            }
    except requests.exceptions.Timeout:
        logger.error("Ollama request timeout")
        return {
            "status": "failed",
            "error": "Ollama request timed out",
            "timeout_seconds": OLLAMA_TIMEOUT,
            "suggestion": "Increase OLLAMA_TIMEOUT in .env or check if Ollama is responsive"
        }
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Cannot connect to Ollama: {e}")
        return {
            "status": "failed",
            "error": f"Cannot connect to Ollama at {OLLAMA_BASE_URL}",
            "suggestion": "Make sure Ollama is running: ollama serve"
        }
    except Exception as e:
        logger.error(f"Ollama test error: {e}")
        return {
            "status": "failed",
            "error": str(e),
            "suggestion": "Check Ollama logs"
        }
