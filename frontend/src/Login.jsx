import { useState } from "react";

export default function Login({ setUser, setShowReg }) {
  const [email,setEmail]=useState("");
  const [password,setPassword]=useState("");

  const login = async () => {
    const r = await fetch("http://localhost:5000/login",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({email,password})
    });
    setUser(await r.json());
  };

  return (
    <div className="card">
      <h2>Login</h2>
      <input placeholder="Email" onChange={e=>setEmail(e.target.value)} />
      <input placeholder="Password" type="password" onChange={e=>setPassword(e.target.value)} />
      <button onClick={login}>Login</button>
      <button onClick={()=>setShowReg(true)}>Register</button>
    </div>
  );
}
