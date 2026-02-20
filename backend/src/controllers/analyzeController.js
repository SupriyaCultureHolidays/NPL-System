import { callPythonNLP } from "../modules/pythonService.js";
import axios from "axios";
import FormData from "form-data";

export const analyzeText = async (req, res) => {
    const { text, features, question } = req.body;
    console.log(req.body);

    if (req.file) {
        try {
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
            const resp = await axios.post("http://localhost:5000/analyze", form, {
                headers: form.getHeaders()
            });
            return res.json(resp.data);
        } catch (err) {
            console.error("Python multipart error:", err.message);
            return res.status(500).json({ error: "Upload analyze failed" });
        }
    }

    if (!text) return res.status(400).json({ error: "Text is required" });

    try {
        const result = await callPythonNLP({ text, question, features });

        res.json(result);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
};
