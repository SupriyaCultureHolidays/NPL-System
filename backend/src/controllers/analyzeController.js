import { callPythonNLP } from "../modules/pythonService.js";
import axios from "axios";
import FormData from "form-data";

export const analyzeText = async (req, res) => {
    const { text, features, question } = req.body;
    console.log("📨 Request received:", { text: text ? "✓" : "✗", question, file: "✗" });

    if (req.file) {
        try {
            console.log(`📄 Processing file: ${req.file.originalname}`);
            const form = new FormData();
            form.append("file", req.file.buffer, {
                filename: req.file.originalname,
                contentType: req.file.mimetype
            });
            if (question) form.append("question", question);
            if (features) {
                const f = typeof features === "string" ? features : JSON.stringify(features);
                form.append("features", f);
            }
            console.log(`🔗 Sending to Python service (port 5000)...`);
            const resp = await axios.post("http://localhost:5000/analyze", form, {
                headers: form.getHeaders(),
                timeout: 60000
            });
            console.log(`✅ Response from Python service:`, resp.data);
            return res.json(resp.data);
        } catch (err) {
            console.error("❌ Python multipart error:", err.message);
            return res.status(500).json({ error: `Upload analyze failed: ${err.message}` });
        }
    }

    if (!text && !question) return res.status(400).json({ error: "Text or question is required" });

    try {
        console.log(`🔗 Calling Python NLP service...`);
        const result = await callPythonNLP({ text, question, features });
        console.log(`✅ Python service response:`, result);
        res.json(result);
    } catch (err) {
        console.error(`❌ Error:`, err.message);
        res.status(500).json({ error: err.message });
    }
};
