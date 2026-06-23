import Nav from "../components/Nav.jsx";

export default function Dashboard() {
  const usuario = JSON.parse(localStorage.getItem("usuario") || "{}");
  return (
    <>
      <Nav />
      <div className="container">
        <h2>Bienvenido, {usuario.nombre}</h2>
        <p>Sistema Integral de Gestión de Biblioteca Universitaria — UNAM FCA.</p>
      </div>
    </>
  );
}
