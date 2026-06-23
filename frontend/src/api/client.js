const BASE_URL = "http://localhost:5000/api";

function authHeaders() {
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
      ...options.headers,
    },
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Error en la petición");
  return data;
}

export const api = {
  login: (correo, password) =>
    request("/auth/login", { method: "POST", body: JSON.stringify({ correo, password }) }),

  getLibros: () => request("/libros"),
  crearLibro: (libro) => request("/libros", { method: "POST", body: JSON.stringify(libro) }),

  getUsuarios: () => request("/usuarios"),
  crearUsuario: (usuario) => request("/usuarios", { method: "POST", body: JSON.stringify(usuario) }),

  getPrestamos: () => request("/prestamos"),
  crearPrestamo: (prestamo) => request("/prestamos", { method: "POST", body: JSON.stringify(prestamo) }),
  devolverPrestamo: (id) => request(`/prestamos/${id}/devolucion`, { method: "POST" }),

  reporteLibrosPrestados: () => request("/reportes/libros-prestados"),
  reporteLibrosDisponibles: () => request("/reportes/libros-disponibles"),
  reporteUsuariosConPrestamos: () => request("/reportes/usuarios-con-prestamos"),
};
