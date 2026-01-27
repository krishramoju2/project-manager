import { useState } from "react";
import Login from "./Login";
import Register from "./Register";
import Dashboard from "./Dashboard";

export default function App() {
  const [user, setUser] = useState(null);
  const [showReg, setShowReg] = useState(false);

  if (!user)
    return showReg
      ? <Register setShowReg={setShowReg} />
      : <Login setUser={setUser} setShowReg={setShowReg} />;

  return <Dashboard user={user} />;
}
