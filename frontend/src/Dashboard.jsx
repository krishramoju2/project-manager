import { useEffect, useState } from "react";

export default function Dashboard({ user }) {
  const [projects, setProjects] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [productivity, setProductivity] = useState(null);

  useEffect(() => {
    fetch("http://localhost:5000/projects")
      .then(r => r.json())
      .then(setProjects);

    fetch(`http://localhost:5000/tasks/${user.id}/${user.role}`)
      .then(r => r.json())
      .then(setTasks);

    // ---- FETCH PRODUCTIVITY (ONLY FOR EMPLOYEE) ----
    if (user.role === "employee") {
      fetch(`http://localhost:5000/productivity/${user.id}`)
        .then(r => r.json())
        .then(setProductivity);
    }
  }, []);

  return (
    <div className="container">
      <h2>{user.role.toUpperCase()} DASHBOARD</h2>

      {/* ---- PRODUCTIVITY SCORE ---- */}
      {user.role === "employee" && productivity && (
        <div className="card">
          <h3>Productivity Score</h3>
          <p>
            Completed {productivity.completed} out of {productivity.total} tasks
          </p>
          <b>{productivity.score}%</b>
        </div>
      )}

      {/* ---- PROJECTS (MANAGER) ---- */}
      {user.role === "manager" &&
        projects.map(p => (
          <div className="card" key={p[0]}>
            {p[1]} ({p[2]})
            <button
              onClick={() =>
                fetch(
                  `http://localhost:5000/project/complete/${p[0]}`,
                  { method: "POST" }
                )
              }
            >
              Complete
            </button>
          </div>
        ))}

      <h3>Tasks</h3>

      {tasks.map(t => (
        <div className="card" key={t[0]}>
          <b>{t[1]}</b>
          <p>{t[2]}</p>
          <p>Status: {t[3]}</p>

          {user.role === "employee" && t[3] !== "completed" && (
            <button
              onClick={() =>
                fetch(
                  `http://localhost:5000/task/complete/${t[0]}`,
                  { method: "POST" }
                )
              }
            >
              Done
            </button>
          )}
        </div>
      ))}
    </div>
  );
}
