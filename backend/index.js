import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import analyzeRoutes from "./src/routes/analyzeRoutes.js";

// Load environment variables
dotenv.config();

const app = express();

// Configuration
const CORS_ORIGIN = process.env.CORS_ORIGIN || "http://localhost:3000";
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors({
    origin: CORS_ORIGIN,
    credentials: true
}));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
app.use("/api", analyzeRoutes);

// Health check
app.get("/", (req, res) => {
    res.json({
        message: "Welcome to NPL System",
        status: "running",
        version: "1.0.0",
        services: {
            backend: "running",
            pythonService: process.env.PYTHON_SERVICE_URL || "http://localhost:5000"
        }
    });
});

// Health endpoint
app.get("/health", (req, res) => {
    res.json({
        status: "healthy",
        timestamp: new Date().toISOString(),
        environment: {
            nodeEnv: process.env.NODE_ENV || "development",
            pythonServiceUrl: process.env.PYTHON_SERVICE_URL || "http://localhost:5000",
            corsOrigin: CORS_ORIGIN
        }
    });
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error("Error:", err.message);
    res.status(500).json({
        error: err.message,
        status: "error" 
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`✓ Server running on port ${PORT}`);
    console.log(`✓ CORS enabled for: ${CORS_ORIGIN}`);
    console.log(`✓ Python Service: ${process.env.PYTHON_SERVICE_URL || "http://localhost:5000"}`);
});
