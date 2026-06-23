import { useState } from "react";
import Nav from "../components/Nav.jsx";
import { api } from "../api/client.js";

const REPORTES = {
  "Libros prestados": (api) => api.reporteLibrosPrestados(),
  "Libros disponibles": (api) => api.reporteLibrosDisponibles(),
  "Usuarios con préstamos activos": (api) => api.reporteUsuariosConPrestamos(),
};

const COLUMNAS = {
  libros_prestados: [
    { key: "id", label: "ID" },
    { key: "usuario_id", label: "ID Usuario" },
    { key: "libro_id", label: "ID Libro" },
    { key: "fecha_prestamo", label: "Fecha préstamo" },
    { key: "fecha_devolucion_esperada", label: "Devolución esperada" },
    { key: "estado", label: "Estado" },
  ],
  libros_disponibles: [
    { key: "id", label: "ID" },
    { key: "titulo", label: "Título" },
    { key: "autor", label: "Autor" },
    { key: "isbn", label: "ISBN" },
    { key: "categoria", label: "Categoría" },
    { key: "copias_disponibles", label: "Disponibles" },
    { key: "copias_totales", label: "Total" },
  ],
  usuarios_con_prestamos_activos: [
    { key: "id", label: "ID" },
    { key: "nombre", label: "Nombre" },
    { key: "correo", label: "Correo" },
    { key: "tipo", label: "Tipo" },
  ],
};

function formatVal(val) {
  if (val === null || val === undefined) return "—";
  if (typeof val === "boolean") return val ? "Sí" : "No";
  if (typeof val === "string" && val.includes("T")) {
    const d = new Date(val);
    if (!isNaN(d)) return d.toLocaleDateString("es-MX");
  }
  return val;
}

export default function Reportes() {
  const [resultado, setResultado] = useState(null);
  const [activo, setActivo] = useState("");
  const [error, setError] = useState("");

  const ejecutar = async (nombre) => {
    setError("");
    setActivo(nombre);
    try {
      const data = await REPORTES[nombre](api);
      setResultado(data);
    } catch (err) {
      setError(err.message);
    }
  };

  const columnas = resultado ? COLUMNAS[resultado.tipo] || [] : [];

  return (
    <>
      <Nav />
      <div className="container">
        <h2>Reportes</h2>
        <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1.5rem", flexWrap: "wrap" }}>
          {Object.keys(REPORTES).map((nombre) => (
            <button
              key={nombre}
              onClick={() => ejecutar(nombre)}
              style={{ opacity: activo === nombre ? 1 : 0.75 }}
            >
              {nombre}
            </button>
          ))}
        </div>

        {error && <p className="error">{error}</p>}

        {resultado && (
          <>
            <p style={{ marginBottom: "0.5rem" }}>
              <strong>Total de registros:</strong> {resultado.total}
            </p>
            {resultado.total === 0 ? (
              <p style={{ color: "var(--verde-carbon)", fontStyle: "italic" }}>
                No hay datos para mostrar en este reporte.
              </p>
            ) : (
              <table>
                <thead>
                  <tr>
                    {columnas.map((col) => (
                      <th key={col.key}>{col.label}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {resultado.datos.map((fila, i) => (
                    <tr key={i}>
                      {columnas.map((col) => (
                        <td key={col.key}>{formatVal(fila[col.key])}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </>
        )}
      </div>
    </>
  );
}
