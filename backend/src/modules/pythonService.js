import axios from "axios";

// Get Python service URL from environment or use default
const PYTHON_SERVICE_URL = process.env.PYTHON_SERVICE_URL || "http://localhost:5000";

export const callPythonNLP = async (payload) => {
    try {
        const response = await axios.post(
            `${PYTHON_SERVICE_URL}/analyze`,
            payload,
            {
                headers: { "Content-Type": "application/json" },
                timeout: 60000 // 60 second timeout for long-running requests
            }
        );
        return response.data;
    } catch (err) {
        console.error("Python service error:", err.message);
        if (err.response) {
            console.error("Response status:", err.response.status);
            console.error("Response data:", err.response.data);
        }
        throw new Error(`Python NLP service failed: ${err.message}`);
    }
};
