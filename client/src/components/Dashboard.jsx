import React, { useState, useEffect } from "react";
import ScientistCard from "./ScientistCard";
import ScientistForm from "./ScientistForm";

function Dashboard() {
  const [scientists, setScientists] = useState([]);

  useEffect(() => {
    const fetchScientists = async () => {
      const response = await fetch("/scientists");
      const sciArr = await response.json();
      setScientists(sciArr);
    };
    fetchScientists().catch(console.error);
  }, []);

  function handleAddScientist(newSci) {
    setScientists((scientists) => [...scientists, newSci]);
  }

  function handleDeleteScientist(id) {
    fetch(`/scientists/${id}`, { method: "DELETE" }).then((r) => {
      if (r.ok) {
        setScientists((scientists) =>
          scientists.filter((sci) => sci.id !== id)
        );
      }
    });
  }

  const sciCards = scientists.map((sci) => (
    <ScientistCard
      key={sci.id}
      scientist={sci}
      onDelete={handleDeleteScientist}
    />
  ));

  return (
    <>
      <h1>Scientists</h1>
      <div className="sciList">{sciCards}</div>
      <hr />
      <ScientistForm onScientistRequest={handleAddScientist} edit={false} />
    </>
  );
}

export default Dashboard;
