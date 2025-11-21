// Manejo de tabs
const tabs = document.querySelectorAll(".tab-btn");
const forms = document.querySelectorAll(".auth-form");

tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    tabs.forEach((t) => t.classList.remove("active"));
    forms.forEach((f) => f.classList.remove("active"));
    tab.classList.add("active");
    document.getElementById(tab.dataset.tab).classList.add("active");
  });
});

// Registro de usuario
document.getElementById("register").addEventListener("submit", async function (e) {
  e.preventDefault();

  const nombre = this.querySelector("input[placeholder='Nombre completo']").value;
  const correo = this.querySelector("input[placeholder='Correo electrónico']").value;
  const contrasena = this.querySelector("input[placeholder='Contraseña']").value;
  const confirmar = this.querySelector("input[placeholder='Confirmar contraseña']").value;

  if (contrasena !== confirmar) {
    alert("Las contraseñas no coinciden");
    return;
  }

  const data = {
    nombre: nombre,
    correo: correo,
    contrasena: contrasena
  };

  try {
    const response = await fetch("/api/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (response.ok) {
      alert("Cuenta creada con éxito");
      window.location.href = "/login"; // o donde quieras redirigir
    } else {
      alert("Error: " + result.error);
    }
  } catch (error) {
    alert("Error de conexión con el servidor");
    console.error(error);
  }
});
