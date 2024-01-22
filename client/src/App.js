import React from "react";
import { Route, Routes } from "react-router-dom";
import Dashboard from "./components/Dashboard";
import Header from "./components/Header";
import ScientistDetail from "./components/ScientistDetail";

function App() {
  return (
    <div>
      <Header />
      <main>
        <Routes>
          <Route index element={<Dashboard />} />
          <Route path="/scientists/:id/*" element={<ScientistDetail />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
