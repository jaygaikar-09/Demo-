import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import pool from "./db.js";

dotenv.config();
const app = express();
app.use(cors());
app.use(express.json());

// GET all topics
app.get("/api/topics", async (req, res) => {
  const [rows] = await pool.query("SELECT * FROM topics ORDER BY date DESC");
  res.json(rows);
});

// POST add a topic
app.post("/api/topics", async (req, res) => {
  const { name, score, date } = req.body;
  const [result] = await pool.query(
    "INSERT INTO topics (name, score, date) VALUES (?, ?, ?)",
    [name, score, date]
  );

  if (score < 60) {
    await pool.query(
      "INSERT IGNORE INTO weak_areas (topic) VALUES (?)", [name]
    );
  } else {
    await pool.query(
      "DELETE FROM weak_areas WHERE topic = ?", [name]
    );
  }

  res.json({ id: result.insertId, name, score, date });
});

// GET weak areas
app.get("/api/weak-areas", async (req, res) => {
  const [rows] = await pool.query("SELECT topic FROM weak_areas");
  res.json(rows.map(r => r.topic));
});

// DELETE a topic
app.delete("/api/topics/:id", async (req, res) => {
  await pool.query("DELETE FROM topics WHERE id = ?", [req.params.id]);
  res.json({ success: true });
});

app.listen(process.env.PORT, () => {
  console.log(`Server running on http://localhost:${process.env.PORT}`);
});