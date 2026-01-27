import { useState } from "react";

export default function Register({ setShowReg }) {
  const [f,setF]=useState({});

  const reg = async () => {
    await fetch("http://localhost:5000/register",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify(f)
    });
    setShowReg(false);
  };

  return (
    <div className="card">
      <h2>Register</h2>
      <input placeholder="Name" onChange={e=>setF({...f,name:e.target.value})}/>
      <input placeholder="Email" onChange={e=>setF({...f,email:e.target.value})}/>
      <input placeholder="Password" type="password" onChange={e=>setF({...f,password:e.target.value})}/>
      <select onChange={e=>setF({...f,role:e.target.value})}>
        <option>employee</option>
        <option>manager</option>
      </select>
      <button onClick={reg}>Create</button>
    </div>
  );
}
