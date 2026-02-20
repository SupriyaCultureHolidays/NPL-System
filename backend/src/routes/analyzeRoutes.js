import express from "express";
import multer from "multer";
import { analyzeText } from "../controllers/analyzeController.js";

const router = express.Router();
const upload = multer({ storage: multer.memoryStorage() });

router.post("/analyze", upload.single("file"), analyzeText);

export default router;
