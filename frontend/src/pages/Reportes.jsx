import { useState } from "react";
import Nav from "../components/Nav.jsx";
import { api } from "../api/client.js";

const REPORTES = {
  "Libros prestados": api => api.reporteLibrosPrestados(),
  "Libros disponibles": api => api.reporteLibrosDisponibles(),
  "Usuarios con préstamos activos": api => api.reporteUsuariosConPrestamos(),
};

export default function Reportes() {
  const [resultado, setResultado] = useState(null);
  const [error, setError] = useState("");

  const ejecutar = async (nombre) => {
    setError("");
    try {
      const data = await REPORTES[nombre](api);
      setResultado(data);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <>
      <Nav />
      <div className="container">
        <h2>Reportes</h2>
        <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem" }}>
          {Object.keys(REPORTES).map((nombre) => (
            <button key={nombre} onClick={() => ejecutar(nombre)}>{nombre}</button>
          ))}
        </div>
        {error && <p className="error">{error}</p>}
        {resultado && (
          <>
            <p>Total: {resultado.total}</p>
            <pre style={{ background: "white", padding: "1rem", overflowX: "auto" }}>
              {JSON.stringify(resultado.datos, null, 2)}
            </pre>
          </>
        )}
      </div>
    </>
  );
}
