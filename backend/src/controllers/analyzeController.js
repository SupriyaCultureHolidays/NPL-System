import { callPythonNLP } from "../modules/pythonService.js";

export const analyzeText = async (req, res) => {
    const { text, features, question } = req.body;
    console.log(req.body)

    if (!text) return res.status(400).json({ error: "Text is required" });

    try {
        const result = await callPythonNLP({ text, question, features });

        res.json(result);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
};
