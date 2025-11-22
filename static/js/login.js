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

document.getElementById("login").addEventListener("submit", async function (e) {
  e.preventDefault();

  const correo = this.querySelector(
    "input[placeholder='Correo electrónico']"
  ).value;
  const contrasena = this.querySelector(
    "input[placeholder='Contraseña']"
  ).value;

  const data = {
    correo: correo,
    contrasena: contrasena,
  };

  try {
    const response = await fetch("/api/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (response.ok) {
      alert("Inicio de sesión exitoso");
      window.location.href = "/inicial";
    } else {
      alert("Error: " + result.error);
    }
  } catch (error) {
    alert("Error de conexión con el servidor");
    console.error(error);
  }
});

document
  .getElementById("register")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const nombre = document.getElementById("reg_nombre").value;
    const correo = document.getElementById("reg_correo").value;
    const contrasena = document.getElementById("reg_pass").value;
    const confirmar = document.getElementById("reg_pass2").value;

    if (contrasena !== confirmar) {
      alert("Las contraseñas no coinciden");
      return;
    }

    const data = {
      nombre: nombre,
      correo: correo,
      contrasena: contrasena,
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
        window.location.href = "/login";
      } else {
        alert("Error: " + result.error);
      }
    } catch (error) {
      alert("Error de conexión con el servidor");
      console.error(error);
    }
  });
