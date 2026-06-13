export function generateStudyPlan(topicsLearned, weakAreas, quizScores) {
  const today = new Date();
  const plan = {};

  const allTopics = [
    "Arrays", "Linked List", "Binary Search",
    "Recursion", "Sorting", "Trees", "Graphs", "Dynamic Programming"
  ];

  // Topics not yet covered
  const covered = topicsLearned.map(t => t.name);
  const newTopics = allTopics.filter(t => !covered.includes(t));

  // Build next 3 days
  for (let i = 0; i < 3; i++) {
    const date = new Date(today);
    date.setDate(today.getDate() + i);
    const label = i === 0 ? "Today" : i === 1 ? "Tomorrow" : date.toLocaleDateString("en-US", { weekday: "long" });

    const sessions = [];

    // Prioritize weak areas
    weakAreas.forEach(topic => {
      sessions.push({ topic, duration: 30, type: "Revision", priority: "high" });
    });

    // Add a new topic if available
    if (newTopics[i]) {
      sessions.push({ topic: newTopics[i], duration: 25, type: "New Topic", priority: "normal" });
    }

    // Add quiz on day 2
    if (i === 2) {
      sessions.push({ topic: "Mixed Quiz", duration: 20, type: "Quiz", priority: "normal" });
    }

    plan[label] = sessions;
  }

  return plan;
}