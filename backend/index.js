import express from "express";
import analyzeRoutes from "./src/routes/analyzeRoutes.js";

const app = express();
app.use(express.json());

app.use("/api", analyzeRoutes);
app.get("/", (req, res) => {
    res.send("Welcome to NPL System")
})

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));