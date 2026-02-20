import axios from "axios";

export const callPythonNLP = async (payload) => {
    try {
        const response = await axios.post("http://localhost:5000/analyze", payload, {
            headers: { "Content-Type": "application/json" }
        });
        return response.data;
    } catch (err) {
        console.error("Python service error:", err.message);
        throw new Error("Python NLP service failed");
    }
};
