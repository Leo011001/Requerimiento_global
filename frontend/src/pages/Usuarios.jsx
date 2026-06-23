import { useEffect, useState } from "react";
import Nav from "../components/Nav.jsx";
import { api } from "../api/client.js";

export default function Usuarios() {
  const [usuarios, setUsuarios] = useState([]);
  const [form, setForm] = useState({ nombre: "", correo: "", password: "", tipo: "alumno" });
  const [error, setError] = useState("");

  const cargar = () => api.getUsuarios().then(setUsuarios).catch((e) => setError(e.message));

  useEffect(() => { cargar(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await api.crearUsuario(form);
      setForm({ nombre: "", correo: "", password: "", tipo: "alumno" });
      cargar();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <>
      <Nav />
      <div className="container">
        <h2>Usuarios</h2>
        <form onSubmit={handleSubmit}>
          <input placeholder="Nombre" value={form.nombre} onChange={(e) => setForm({ ...form, nombre: e.target.value })} required />
          <input type="email" placeholder="Correo" value={form.correo} onChange={(e) => setForm({ ...form, correo: e.target.value })} required />
          <input type="password" placeholder="Contraseña" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
          <select value={form.tipo} onChange={(e) => setForm({ ...form, tipo: e.target.value })}>
            <option value="alumno">Alumno</option>
            <option value="bibliotecario">Bibliotecario</option>
            <option value="admin">Admin</option>
          </select>
          {error && <p className="error">{error}</p>}
          <button type="submit">Crear usuario</button>
        </form>

        <table>
         <thead><tr><th>ID</th><th>Nombre</th><th>Correo</th><th>Tipo</th><th>Activo</th></tr></thead>
          <tbody>
            {usuarios.map((u) => (
             <tr key={u.id}><td>{u.id}</td><td>{u.nombre}</td><td>{u.correo}</td><td>{u.tipo}</td><td>{u.activo ? "Sí" : "No"}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
