from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from pydantic import BaseModel
import spacy
import pdfplumber
import json
from typing import Optional, Dict, Any

nlp = spacy.load("en_core_web_sm")

app = FastAPI(title="Python NLP Service")

class TextRequest(BaseModel):
    text: str

def _extract_text_from_upload(file: UploadFile) -> str:
    name = (file.filename or "").lower()
    if name.endswith(".pdf") or (file.content_type or "") == "application/pdf":
        with pdfplumber.open(file.file) as pdf:
            return "".join([p.extract_text() or "" for p in pdf.pages])
    return file.file.read().decode("utf-8", errors="ignore")

def _answer_from_text(text: str, question: str) -> Dict[str, Any]:
    d = nlp(text)
    q = nlp(question)
    qset = {t.lemma_.lower() for t in q if not t.is_stop and not t.is_punct}
    best_score = 0.0
    best_sent = ""
    for s in d.sents:
        sset = {t.lemma_.lower() for t in s if not t.is_stop and not t.is_punct}
        overlap = len(qset & sset)
        score = overlap / (len(qset) or 1)
        if score > best_score:
            best_score = score
            best_sent = s.text
    return {"answer": best_sent.strip(), "confidence": round(best_score, 3)}

@app.post("/analyze")
async def analyze(
    request: Request,
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    question: Optional[str] = Form(None),
    features: Optional[str] = Form(None),
):
    data = None
    ct = request.headers.get("content-type", "")
    if "application/json" in ct:
        data = await request.json()
        text = data.get("text")
        question = data.get("question")
        features = data.get("features")
    if file:
        text = _extract_text_from_upload(file)
    if not text:
        raise HTTPException(status_code=400, detail="Text or file is required")
    doc = nlp(text)

    result = {
        "tokens": [token.text for token in doc],
        "pos": [{token.text: token.pos_} for token in doc],
        "entities": [{"text": ent.text, "label": ent.label_} for ent in doc.ents],  # <-- FIXED
        "lemmas": [{token.text: token.lemma_} for token in doc],
        "dependencies": [
            {"token": token.text, "dep": token.dep_, "head": token.head.text} 
            for token in doc
        ],
    }

    if question:
        qa = _answer_from_text(text, question)
        result["answer"] = qa["answer"]
        result["confidence"] = qa["confidence"]

    if features:
        try:
            feats = features if isinstance(features, dict) else json.loads(features)
        except Exception:
            feats = None
        if isinstance(feats, dict):
            filtered = {}
            for k, v in feats.items():
                if v and k in result:
                    filtered[k] = result[k]
            if question:
                filtered["answer"] = result.get("answer")
                filtered["confidence"] = result.get("confidence")
            return filtered

    return result

@app.post("/api/analyze")
async def analyze_api(
    request: Request,
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    question: Optional[str] = Form(None),
    features: Optional[str] = Form(None),
):
    return await analyze(request, file, text, question, features)

@app.get("/")
def root():
    return {"status": "ok"}
