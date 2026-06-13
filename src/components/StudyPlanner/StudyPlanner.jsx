import React, { useState, useEffect } from "react";
import { initialStudyData } from "../../data/studyData";
import { generateStudyPlan } from "./plannerUtils";

const API = "http://localhost:5000/api";

const priorityColor = {
  high: "bg-red-100 border-red-400 text-red-700",
  normal: "bg-blue-50 border-blue-300 text-blue-700",
};

const typeIcon = {
  Revision: "🔁",
  "New Topic": "📘",
  Quiz: "🧪",
};

export default function StudyPlanner() {
  const [topics, setTopics] = useState(initialStudyData.topicsLearned);
  const [weakAreas, setWeakAreas] = useState(initialStudyData.weakAreas);
  const [newTopic, setNewTopic] = useState("");
  const [newScore, setNewScore] = useState("");
  const [activeDay, setActiveDay] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [topicsRes, weakAreasRes] = await Promise.all([
          fetch(`${API}/topics`),
          fetch(`${API}/weak-areas`),
        ]);

        if (!topicsRes.ok || !weakAreasRes.ok) {
          throw new Error("Backend unavailable");
        }

        const topicsData = await topicsRes.json();
        const weakAreasData = await weakAreasRes.json();

        setTopics(topicsData.length ? topicsData : initialStudyData.topicsLearned);
        setWeakAreas(weakAreasData.length ? weakAreasData : initialStudyData.weakAreas);
      } catch (error) {
        setTopics(initialStudyData.topicsLearned);
        setWeakAreas(initialStudyData.weakAreas);
      }
    };

    loadData();
  }, []);

  const quizScores = Object.fromEntries(topics.map(t => [t.name, t.score]));
  const plan = generateStudyPlan(topics, weakAreas, quizScores);
  const days = Object.keys(plan);

  useEffect(() => {
    if (days.length > 0 && !activeDay) setActiveDay(days[0]);
  }, [days]);

  const addTopic = async () => {
    const score = parseInt(newScore);
    if (!newTopic || isNaN(score)) return;

    const date = new Date().toISOString().split("T")[0];
    const res = await fetch(`${API}/topics`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: newTopic, score, date }),
    });
    const saved = await res.json();
    setTopics(prev => [saved, ...prev]);
    fetch(`${API}/weak-areas`).then(r => r.json()).then(setWeakAreas);
    setNewTopic("");
    setNewScore("");
  };

  const totalTime = activeDay
    ? plan[activeDay].reduce((sum, s) => sum + s.duration, 0) : 0;

  const avgScore = topics.length > 0
    ? Math.round(topics.reduce((s, t) => s + t.score, 0) / topics.length) : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 p-6 font-sans">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-indigo-900 tracking-tight">📅 Study Planner</h1>
          <p className="text-indigo-400 mt-1 text-sm">Adaptive schedule based on your performance</p>
        </div>

        <div className="grid grid-cols-3 gap-4 mb-8">
          <StatCard label="Topics Covered" value={topics.length} icon="📚" color="indigo" />
          <StatCard label="Avg Quiz Score" value={`${avgScore}%`} icon="🎯" color="purple" />
          <StatCard label="Weak Areas" value={weakAreas.length} icon="⚠️" color="rose" />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-1 space-y-5">
            <div className="bg-white rounded-2xl shadow-sm border border-red-100 p-4">
              <h2 className="font-semibold text-gray-700 mb-3">⚠️ Weak Areas</h2>
              {weakAreas.length === 0 ? (
                <p className="text-gray-400 text-sm">No weak areas — great job!</p>
              ) : (
                <div className="flex flex-wrap gap-2">
                  {weakAreas.map(area => (
                    <span key={area} className="bg-red-50 text-red-600 border border-red-200 text-xs px-3 py-1 rounded-full font-medium">
                      {area}
                    </span>
                  ))}
                </div>
              )}
            </div>

            <div className="bg-white rounded-2xl shadow-sm border border-indigo-100 p-4">
              <h2 className="font-semibold text-gray-700 mb-3">➕ Log a Topic</h2>
              <input
                className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm mb-2 focus:outline-none focus:ring-2 focus:ring-indigo-300"
                placeholder="Topic name"
                value={newTopic}
                onChange={e => setNewTopic(e.target.value)}
              />
              <input
                className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm mb-3 focus:outline-none focus:ring-2 focus:ring-indigo-300"
                placeholder="Quiz score (0-100)"
                type="number"
                value={newScore}
                onChange={e => setNewScore(e.target.value)}
              />
              <button
                onClick={addTopic}
                className="w-full bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium py-2 rounded-lg transition-colors"
              >
                Save Topic
              </button>
            </div>

            <div className="bg-white rounded-2xl shadow-sm border border-purple-100 p-4">
              <h2 className="font-semibold text-gray-700 mb-3">📚 Topics Learned</h2>
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {topics.length === 0 ? (
                  <p className="text-gray-400 text-sm">No topics yet — add one!</p>
                ) : (
                  topics.map(t => (
                    <div key={t.id} className="flex justify-between items-center text-sm py-1 border-b border-gray-50">
                      <span className="text-gray-700">{t.name}</span>
                      <span className={`font-bold ${t.score >= 70 ? "text-green-500" : t.score >= 50 ? "text-yellow-500" : "text-red-500"}`}>
                        {t.score}%
                      </span>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>

          <div className="md:col-span-2">
            <div className="bg-white rounded-2xl shadow-sm border border-indigo-100 p-5">
              <h2 className="font-semibold text-gray-700 mb-4">🗓️ Your Study Schedule</h2>
              <div className="flex gap-2 mb-5">
                {days.map(day => (
                  <button
                    key={day}
                    onClick={() => setActiveDay(day)}
                    className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
                      activeDay === day
                        ? "bg-indigo-600 text-white"
                        : "bg-indigo-50 text-indigo-600 hover:bg-indigo-100"
                    }`}
                  >
                    {day}
                  </button>
                ))}
              </div>
              {activeDay && (
                <>
                  <p className="text-xs text-gray-400 mb-3">⏱ Total: {totalTime} mins</p>
                  <div className="space-y-3">
                    {plan[activeDay].map((session, i) => (
                      <div key={i} className={`flex items-center justify-between border rounded-xl px-4 py-3 ${priorityColor[session.priority]}`}>
                        <div className="flex items-center gap-3">
                          <span className="text-xl">{typeIcon[session.type]}</span>
                          <div>
                            <p className="font-semibold text-sm">{session.topic}</p>
                            <p className="text-xs opacity-70">{session.type}</p>
                          </div>
                        </div>
                        <span className="text-sm font-bold">{session.duration} min</span>
                      </div>
                    ))}
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ label, value, icon, color }) {
  const colors = {
    indigo: "bg-indigo-50 text-indigo-700 border-indigo-100",
    purple: "bg-purple-50 text-purple-700 border-purple-100",
    rose: "bg-rose-50 text-rose-700 border-rose-100",
  };
  return (
    <div className={`rounded-2xl border p-4 ${colors[color]}`}>
      <div className="text-2xl mb-1">{icon}</div>
      <div className="text-2xl font-bold">{value}</div>
      <div className="text-xs opacity-70 mt-0.5">{label}</div>
    </div>
  );
}