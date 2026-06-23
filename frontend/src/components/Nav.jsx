import { Link, useNavigate } from "react-router-dom";

export default function Nav() {
  const navigate = useNavigate();
  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };
  return (
    <nav>
      <Link to="/">Inicio</Link>
      <Link to="/libros">Libros</Link>
      <Link to="/usuarios">Usuarios</Link>
      <Link to="/prestamos">Préstamos</Link>
      <Link to="/reportes">Reportes</Link>
      <a href="#" onClick={logout} style={{ marginLeft: "auto" }}>Salir</a>
    </nav>
  );
}
