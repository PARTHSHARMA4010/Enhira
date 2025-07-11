import { useEffect, useState } from "react";

function App() {
  const [backendOk, setBackendOk] = useState(false);

  useEffect(() => {
    // 1️⃣  quick health-check
    fetch("http://localhost:8000/ping")
      .then((r) => r.json())
      .then((json) => {
        console.log("🟢 Backend replied:", json);      // <— visible in browser dev-tools
        setBackendOk(json.status === "pong");
      })
      .catch(() => console.error("🔴 Backend not reachable"));

    // 2️⃣  load operators (same as before)
    fetch("http://localhost:8000/operators")
      .then((r) => r.json())
      .then((ops) => console.log("Operators list:", ops));
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h2>
        Backend status:&nbsp;
        <span style={{ color: backendOk ? "green" : "red" }}>
          {backendOk ? "ONLINE" : "OFFLINE"}
        </span>
      </h2>
    </div>
  );
}

export default App;
