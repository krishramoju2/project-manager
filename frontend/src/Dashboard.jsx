import { useEffect, useState } from "react";

export default function Dashboard({ user }) {
  const [projects,setProjects]=useState([]);
  const [tasks,setTasks]=useState([]);
  const [emps,setEmps]=useState([]);

  useEffect(()=>{
    fetch("http://localhost:5000/projects").then(r=>r.json()).then(setProjects);
    fetch(`http://localhost:5000/tasks/${user.id}/${user.role}`).then(r=>r.json()).then(setTasks);
    if(user.role==="manager")
      fetch("http://localhost:5000/users").then(r=>r.json()).then(setEmps);
  },[]);

  return (
    <div className="container">
      <h2>{user.role.toUpperCase()} DASHBOARD</h2>

      {user.role==="manager" && projects.map(p=>(
        <div className="card" key={p.id}>
          {p.name} ({p.status})
          <button onClick={()=>fetch(`http://localhost:5000/project/complete/${p.id}`,{method:"POST"})}>
            Complete
          </button>
        </div>
      ))}

      <h3>Tasks</h3>
      {tasks.map(t=>(
        <div className="card" key={t.id}>
          <b>{t.title}</b>
          <p>{t.description}</p>
          <p>{t.status}</p>
          {user.role==="employee" &&
            <button onClick={()=>fetch(`http://localhost:5000/task/complete/${t.id}`,{method:"POST"})}>
              Done
            </button>}
        </div>
      ))}
    </div>
  );
}
