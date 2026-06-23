import { useEffect, useState } from "react";
import Nav from "../components/Nav.jsx";
import { api } from "../api/client.js";

export default function Prestamos() {
  const [prestamos, setPrestamos] = useState([]);
  const [form, setForm] = useState({ usuario_id: "", libro_id: "", dias: 7 });
  const [error, setError] = useState("");

  const cargar = () => api.getPrestamos().then(setPrestamos).catch((e) => setError(e.message));

  useEffect(() => { cargar(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await api.crearPrestamo({
        usuario_id: Number(form.usuario_id),
        libro_id: Number(form.libro_id),
        dias: Number(form.dias),
      });
      setForm({ usuario_id: "", libro_id: "", dias: 7 });
      cargar();
    } catch (err) {
      setError(err.message);
    }
  };

  const devolver = async (id) => {
    try {
      await api.devolverPrestamo(id);
      cargar();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <>
      <Nav />
      <div className="container">
        <h2>Préstamos</h2>
        <form onSubmit={handleSubmit}>
          <input placeholder="ID Usuario" value={form.usuario_id} onChange={(e) => setForm({ ...form, usuario_id: e.target.value })} required />
          <input placeholder="ID Libro" value={form.libro_id} onChange={(e) => setForm({ ...form, libro_id: e.target.value })} required />
          <input type="number" placeholder="Días" value={form.dias} onChange={(e) => setForm({ ...form, dias: e.target.value })} />
          {error && <p className="error">{error}</p>}
          <button type="submit">Registrar préstamo</button>
        </form>

        <table>
          <thead><tr><th>ID</th><th>Usuario</th><th>Libro</th><th>Estado</th><th>Devolver</th></tr></thead>
          <tbody>
            {prestamos.map((p) => (
              <tr key={p.id}>
                <td>{p.id}</td><td>{p.usuario_id}</td><td>{p.libro_id}</td><td>{p.estado}</td>
                <td>{p.estado === "activo" && <button onClick={() => devolver(p.id)}>Devolver</button>}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
