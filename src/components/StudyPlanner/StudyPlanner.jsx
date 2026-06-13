import { useState, useEffect } from "react";

const API = "http://localhost:5000/api";

const TOPICS = {
  "🟢 Basics": [
    "Arrays", "Strings", "Linked List", "Stacks", "Queues", "Matrix"
  ],
  "🔵 Searching & Sorting": [
    "Binary Search", "Bubble Sort", "Merge Sort", "Quick Sort",
    "Insertion Sort", "Selection Sort", "Counting Sort", "Radix Sort"
  ],
  "🟣 Recursion & DP": [
    "Recursion", "Backtracking", "Dynamic Programming", "Memoization",
    "Tabulation", "Divide & Conquer", "Greedy Algorithms"
  ],
  "🟠 Trees": [
    "Binary Trees", "Binary Search Tree", "AVL Trees",
    "Segment Trees", "Fenwick Tree", "Trie", "Heap / Priority Queue"
  ],
  "🔴 Graphs": [
    "Graph Basics", "BFS", "DFS", "Shortest Path (Dijkstra)",
    "Bellman Ford", "Floyd Warshall", "Topological Sort",
    "Union Find", "Minimum Spanning Tree"
  ],
  "⚡ Advanced": [
    "Hashing", "Bit Manipulation", "Two Pointers", "Sliding Window",
    "Monotonic Stack", "Interval Problems", "Math & Number Theory",
    "Game Theory", "Computational Geometry"
  ],
};

const ALL_TOPICS = Object.values(TOPICS).flat();

const typeIcon = { Revision: "🔁", "New Topic": "📘", Quiz: "🧪" };
const typeColor = {
  Revision: "bg-rose-50 border-rose-300 text-rose-800",
  "New Topic": "bg-blue-50 border-blue-300 text-blue-800",
  Quiz: "bg-amber-50 border-amber-300 text-amber-800",
};

function generatePlan(topics, weakAreas) {
  const today = new Date();
  const covered = topics.map(t => t.name);
  const newTopics = ALL_TOPICS.filter(t => !covered.includes(t));
  const plan = {};

  for (let i = 0; i < 3; i++) {
    const date = new Date(today);
    date.setDate(today.getDate() + i);
    const label = i === 0 ? "Today" : i === 1 ? "Tomorrow"
      : date.toLocaleDateString("en-US", { weekday: "long" });
    const sessions = [];

    weakAreas.slice(0, 2).forEach(topic => {
      sessions.push({ topic, duration: 30, type: "Revision" });
    });
    if (newTopics[i]) {
      sessions.push({ topic: newTopics[i], duration: 25, type: "New Topic" });
    }
    if (i === 2) {
      sessions.push({ topic: "Mixed Quiz", duration: 20, type: "Quiz" });
    }
    plan[label] = sessions;
  }
  return plan;
}

function ScoreBar({ score }) {
  const color = score >= 70 ? "bg-emerald-400" : score >= 50 ? "bg-amber-400" : "bg-rose-400";
  return (
    <div className="w-full bg-gray-100 rounded-full h-1.5 mt-1">
      <div className={`${color} h-1.5 rounded-full transition-all duration-500`} style={{ width: `${score}%` }} />
    </div>
  );
}

function Toast({ message, onClose }) {
  useEffect(() => {
    const t = setTimeout(onClose, 2500);
    return () => clearTimeout(t);
  }, []);
  return (
    <div className="fixed top-4 right-4 bg-indigo-600 text-white px-5 py-3 rounded-xl shadow-lg text-sm font-medium z-50 animate-bounce">
      {message}
    </div>
  );
}

export default function StudyPlanner() {
  const [topics, setTopics] = useState([]);
  const [weakAreas, setWeakAreas] = useState([]);
  const [newTopic, setNewTopic] = useState("");
  const [newScore, setNewScore] = useState("");
  const [activeDay, setActiveDay] = useState(null);
  const [activeTab, setActiveTab] = useState("planner");
  const [toast, setToast] = useState(null);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch(`${API}/topics`).then(r => r.json()).then(setTopics).catch(() => {
      // fallback to localStorage if backend not running
      const saved = localStorage.getItem("studyPlannerTopics");
      if (saved) setTopics(JSON.parse(saved));
    });
    fetch(`${API}/weak-areas`).then(r => r.json()).then(setWeakAreas).catch(() => {
      const saved = localStorage.getItem("studyPlannerWeak");
      if (saved) setWeakAreas(JSON.parse(saved));
    });
  }, []);

  const plan = generatePlan(topics, weakAreas);
  const days = Object.keys(plan);

  useEffect(() => {
    if (days.length > 0 && !activeDay) setActiveDay(days[0]);
  }, [days]);

  const avgScore = topics.length > 0
    ? Math.round(topics.reduce((s, t) => s + t.score, 0) / topics.length) : 0;

  const totalTime = activeDay
    ? plan[activeDay].reduce((s, t) => s + t.duration, 0) : 0;

  const addTopic = async () => {
    const score = parseInt(newScore);
    if (!newTopic || isNaN(score) || score < 0 || score > 100) {
      setToast("⚠️ Pick a topic and enter score 0–100");
      return;
    }
    if (topics.find(t => t.name === newTopic)) {
      setToast("⚠️ Topic already logged!");
      return;
    }
    setLoading(true);
    const date = new Date().toISOString().split("T")[0];
    try {
      const res = await fetch(`${API}/topics`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: newTopic, score, date }),
      });
      const saved = await res.json();
      const updatedTopics = [saved, ...topics];
      setTopics(updatedTopics);
      localStorage.setItem("studyPlannerTopics", JSON.stringify(updatedTopics));
      const wa = await fetch(`${API}/weak-areas`).then(r => r.json());
      setWeakAreas(wa);
      localStorage.setItem("studyPlannerWeak", JSON.stringify(wa));
    } catch {
      const saved = { id: Date.now(), name: newTopic, score, date };
      const updatedTopics = [saved, ...topics];
      setTopics(updatedTopics);
      localStorage.setItem("studyPlannerTopics", JSON.stringify(updatedTopics));
      const wa = score < 60
        ? [...new Set([...weakAreas, newTopic])]
        : weakAreas.filter(t => t !== newTopic);
      setWeakAreas(wa);
      localStorage.setItem("studyPlannerWeak", JSON.stringify(wa));
    }
    setToast(`✅ ${newTopic} saved!`);
    setNewTopic("");
    setNewScore("");
    setLoading(false);
  };

  const deleteTopic = async (id, name) => {
    try {
      await fetch(`${API}/topics/${id}`, { method: "DELETE" });
    } catch {}
    const updated = topics.filter(t => t.id !== id);
    setTopics(updated);
    localStorage.setItem("studyPlannerTopics", JSON.stringify(updated));
    setToast(`🗑️ ${name} removed`);
  };

  const filteredTopics = topics.filter(t =>
    t.name.toLowerCase().includes(search.toLowerCase())
  );

  const masteredCount = topics.filter(t => t.score >= 70).length;
  const progressPct = ALL_TOPICS.length > 0
    ? Math.round((topics.length / ALL_TOPICS.length) * 100) : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 p-4 md:p-8 font-sans">
      {toast && <Toast message={toast} onClose={() => setToast(null)} />}

      <div className="max-w-5xl mx-auto">

        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white tracking-tight">📅 Study Planner</h1>
            <p className="text-indigo-300 text-sm mt-0.5">Adaptive • Intelligent • Yours</p>
          </div>
          <div className="text-right">
            <div className="text-indigo-300 text-xs">Overall Progress</div>
            <div className="text-white font-bold text-xl">{progressPct}%</div>
            <div className="w-32 bg-slate-700 rounded-full h-1.5 mt-1">
              <div className="bg-indigo-400 h-1.5 rounded-full" style={{ width: `${progressPct}%` }} />
            </div>
          </div>
        </div>

        {/* Stat Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
          {[
            { label: "Topics Logged", value: topics.length, icon: "📚", sub: `of ${ALL_TOPICS.length}` },
            { label: "Avg Score", value: `${avgScore}%`, icon: "🎯", sub: avgScore >= 70 ? "Great!" : "Keep going" },
            { label: "Mastered", value: masteredCount, icon: "🏆", sub: "score ≥ 70%" },
            { label: "Weak Areas", value: weakAreas.length, icon: "⚠️", sub: "need revision" },
          ].map(s => (
            <div key={s.label} className="bg-slate-800 border border-slate-700 rounded-2xl p-4">
              <div className="text-2xl mb-1">{s.icon}</div>
              <div className="text-white font-bold text-xl">{s.value}</div>
              <div className="text-indigo-300 text-xs">{s.label}</div>
              <div className="text-slate-500 text-xs mt-0.5">{s.sub}</div>
            </div>
          ))}
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-5">
          {["planner", "topics", "log"].map(tab => (
            <button key={tab} onClick={() => setActiveTab(tab)}
              className={`px-5 py-2 rounded-full text-sm font-semibold transition-all capitalize ${
                activeTab === tab
                  ? "bg-indigo-500 text-white shadow-lg shadow-indigo-500/30"
                  : "bg-slate-800 text-slate-300 hover:bg-slate-700"
              }`}>
              {tab === "planner" ? "📅 Schedule" : tab === "topics" ? "📚 My Topics" : "➕ Log Topic"}
            </button>
          ))}
        </div>

        {/* PLANNER TAB */}
        {activeTab === "planner" && (
          <div className="bg-slate-800 border border-slate-700 rounded-2xl p-5">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-white font-semibold">Your Study Schedule</h2>
              {weakAreas.length > 0 && (
                <div className="flex gap-1 flex-wrap">
                  {weakAreas.map(w => (
                    <span key={w} className="bg-rose-900/50 text-rose-300 border border-rose-700 text-xs px-2 py-0.5 rounded-full">
                      {w}
                    </span>
                  ))}
                </div>
              )}
            </div>

            <div className="flex gap-2 mb-5">
              {days.map(day => (
                <button key={day} onClick={() => setActiveDay(day)}
                  className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all ${
                    activeDay === day
                      ? "bg-indigo-500 text-white"
                      : "bg-slate-700 text-slate-300 hover:bg-slate-600"
                  }`}>
                  {day}
                </button>
              ))}
            </div>

            {activeDay && (
              <>
                <p className="text-slate-400 text-xs mb-3">⏱ Total study time: {totalTime} mins</p>
                <div className="space-y-3">
                  {plan[activeDay].map((s, i) => (
                    <div key={i} className={`flex items-center justify-between border rounded-xl px-4 py-3 ${typeColor[s.type]}`}>
                      <div className="flex items-center gap-3">
                        <span className="text-2xl">{typeIcon[s.type]}</span>
                        <div>
                          <p className="font-semibold text-sm">{s.topic}</p>
                          <p className="text-xs opacity-60">{s.type}</p>
                        </div>
                      </div>
                      <span className="font-bold text-sm">{s.duration} min</span>
                    </div>
                  ))}
                </div>
              </>
            )}

            {topics.length === 0 && (
              <div className="text-center py-8 text-slate-500">
                <p className="text-4xl mb-2">📖</p>
                <p>Log some topics first to generate your schedule!</p>
              </div>
            )}
          </div>
        )}

        {/* TOPICS TAB */}
        {activeTab === "topics" && (
          <div className="bg-slate-800 border border-slate-700 rounded-2xl p-5">
            <input
              className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-sm text-white mb-4 focus:outline-none focus:ring-2 focus:ring-indigo-500 placeholder-slate-400"
              placeholder="🔍 Search topics..."
              value={search}
              onChange={e => setSearch(e.target.value)}
            />

            {filteredTopics.length === 0 ? (
              <p className="text-slate-500 text-sm text-center py-8">No topics logged yet — go to Log Topic!</p>
            ) : (
              <div className="space-y-2 max-h-96 overflow-y-auto pr-1">
                {filteredTopics.map(t => (
                  <div key={t.id} className="flex items-center justify-between bg-slate-700/50 rounded-xl px-4 py-3 group">
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <span className="text-white text-sm font-medium">{t.name}</span>
                        <span className={`font-bold text-sm ml-4 ${
                          t.score >= 70 ? "text-emerald-400" : t.score >= 50 ? "text-amber-400" : "text-rose-400"
                        }`}>{t.score}%</span>
                      </div>
                      <ScoreBar score={t.score} />
                      <p className="text-slate-500 text-xs mt-1">{t.date}</p>
                    </div>
                    <button
                      onClick={() => deleteTopic(t.id, t.name)}
                      className="ml-4 text-slate-600 hover:text-rose-400 transition-colors opacity-0 group-hover:opacity-100 text-lg"
                    >✕</button>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* LOG TOPIC TAB */}
        {activeTab === "log" && (
          <div className="bg-slate-800 border border-slate-700 rounded-2xl p-5">
            <h2 className="text-white font-semibold mb-4">Log a Completed Topic</h2>

            <div className="space-y-3">
              <div>
                <label className="text-slate-400 text-xs mb-1 block">Select Topic</label>
                <select
                  className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  value={newTopic}
                  onChange={e => setNewTopic(e.target.value)}
                >
                  <option value="">-- Choose a topic --</option>
                  {Object.entries(TOPICS).map(([group, items]) => (
                    <optgroup key={group} label={group}>
                      {items.map(t => (
                        <option key={t} value={t} disabled={!!topics.find(x => x.name === t)}>
                          {t} {topics.find(x => x.name === t) ? "✓" : ""}
                        </option>
                      ))}
                    </optgroup>
                  ))}
                </select>
              </div>

              <div>
                <label className="text-slate-400 text-xs mb-1 block">Quiz Score (0–100)</label>
                <input
                  className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 placeholder-slate-400"
                  placeholder="Enter your score"
                  type="number"
                  min="0" max="100"
                  value={newScore}
                  onChange={e => setNewScore(e.target.value)}
                />
              </div>

              {newScore && (
                <div className={`rounded-lg px-4 py-2 text-sm font-medium ${
                  parseInt(newScore) >= 70 ? "bg-emerald-900/40 text-emerald-300 border border-emerald-700"
                  : parseInt(newScore) >= 50 ? "bg-amber-900/40 text-amber-300 border border-amber-700"
                  : "bg-rose-900/40 text-rose-300 border border-rose-700"
                }`}>
                  {parseInt(newScore) >= 70 ? "🏆 Excellent! Topic mastered."
                    : parseInt(newScore) >= 50 ? "📖 Good effort! A bit more practice needed."
                    : "⚠️ Will be added to weak areas for revision."}
                </div>
              )}

              <button
                onClick={addTopic}
                disabled={loading}
                className="w-full bg-indigo-500 hover:bg-indigo-600 disabled:opacity-50 text-white font-semibold py-2.5 rounded-xl transition-all shadow-lg shadow-indigo-500/20"
              >
                {loading ? "Saving..." : "Save Topic →"}
              </button>
            </div>

            {/* Category overview */}
            <div className="mt-6">
              <h3 className="text-slate-400 text-xs font-semibold mb-3 uppercase tracking-wider">Your Coverage</h3>
              <div className="space-y-2">
                {Object.entries(TOPICS).map(([group, items]) => {
                  const done = items.filter(t => topics.find(x => x.name === t)).length;
                  const pct = Math.round((done / items.length) * 100);
                  return (
                    <div key={group}>
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-slate-300">{group}</span>
                        <span className="text-slate-400">{done}/{items.length}</span>
                      </div>
                      <div className="w-full bg-slate-700 rounded-full h-1.5">
                        <div className="bg-indigo-400 h-1.5 rounded-full transition-all" style={{ width: `${pct}%` }} />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}