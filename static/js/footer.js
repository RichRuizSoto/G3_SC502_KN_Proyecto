document.addEventListener("DOMContentLoaded", () => {
  fetch("footer.html")
    .then(response => response.text())
    .then(data => {
      document.body.insertAdjacentHTML("beforeend", data);
    })
    .catch(err => console.error("Error al cargar el footer:", err));
});
