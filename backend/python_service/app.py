from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from pydantic import BaseModel
import spacy
import pdfplumber
import json
from typing import Optional, Dict, Any, List, Tuple

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
        result["evidence"] = [{"text": s, "score": sc} for s, sc in qa.get("evidence", [])]

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
                if feats.get("evidence"):
                    filtered["evidence"] = result.get("evidence")
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
