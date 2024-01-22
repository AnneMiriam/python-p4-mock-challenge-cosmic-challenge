import { useEffect, useState } from "react";
import { Route, Routes } from "react-router-dom";
import Dashboard from "./components/Dashboard";
import Header from "./components/Header";
import Login from "./components/Login";
import ScientistDetail from "./components/ScientistDetail";
import Signup from "./components/Signup";

function App() {
  const [user, setUser] = useState();

  useEffect(() => {
    fetch("/check_session")
      .then((r) => r.json())
      .then((data) => {
        if (data.id) {
          setUser(data);
        } else {
          setUser(null);
        }
      });
  }, []);

  const logout = () => {
    fetch("/sign_out", { method: "DELETE" }).then(() => {
      setUser(null);
    });
  };

  let view;

  if (user) {
    view = (
      <main>
        <button type="button" onClick={logout}>
          Logout
        </button>
        <Routes>
          <Route index element={<Dashboard />} />
          <Route path="/scientists/:id/*" element={<ScientistDetail />} />
        </Routes>
      </main>
    );
  } else if (user === null) {
    view = (
      <Routes>
        <Route index element={<Login setUser={setUser} />} />
        <Route path="signup" element={<Signup setUser={setUser} />} />
      </Routes>
    );
  } else {
    view = <p>Loading...</p>;
  }

  return (
    <div>
      <Header />
      {view}
    </div>
  );
}

export default App;
