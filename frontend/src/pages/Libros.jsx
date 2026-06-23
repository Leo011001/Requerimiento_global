import { useEffect, useState } from "react";
import Nav from "../components/Nav.jsx";
import { api } from "../api/client.js";

export default function Libros() {
  const [libros, setLibros] = useState([]);
  const [form, setForm] = useState({ titulo: "", autor: "", isbn: "", categoria: "", copias: 1 });
  const [error, setError] = useState("");

  const cargar = () => api.getLibros().then(setLibros).catch((e) => setError(e.message));

  useEffect(() => { cargar(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await api.crearLibro(form);
      setForm({ titulo: "", autor: "", isbn: "", categoria: "", copias: 1 });
      cargar();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <>
      <Nav />
      <div className="container">
        <h2>Libros</h2>
        <form onSubmit={handleSubmit}>
          <input placeholder="Título" value={form.titulo} onChange={(e) => setForm({ ...form, titulo: e.target.value })} required />
          <input placeholder="Autor" value={form.autor} onChange={(e) => setForm({ ...form, autor: e.target.value })} required />
          <input placeholder="ISBN" value={form.isbn} onChange={(e) => setForm({ ...form, isbn: e.target.value })} required />
          <input placeholder="Categoría" value={form.categoria} onChange={(e) => setForm({ ...form, categoria: e.target.value })} />
          <input type="number" min="1" value={form.copias} onChange={(e) => setForm({ ...form, copias: Number(e.target.value) })} />
          {error && <p className="error">{error}</p>}
          <button type="submit">Registrar libro</button>
        </form>

        <table>
          <thead><tr><th>ID</th><th>Título</th><th>Autor</th><th>ISBN</th><th>Disponibles</th></tr></thead>
          <tbody>
            {libros.map((l) => (
             <tr key={l.id}><td>{l.id}</td><td>{l.titulo}</td><td>{l.autor}</td><td>{l.isbn}</td><td>{l.copias_disponibles}/{l.copias_totales}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
