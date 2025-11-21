document.addEventListener("DOMContentLoaded", () => {
  fetch("/header.html")
    .then((response) => {
      if (!response.ok) throw new Error("Error al cargar el header");
      return response.text();
    })
    .then((data) => {
      document.body.insertAdjacentHTML("afterbegin", data);

      const header = document.querySelector(".main-header");
      const main = document.querySelector("main");

      if (header && main) {
        const ajustarMain = () => main.style.paddingTop = header.offsetHeight + "px";

        ajustarMain();
        window.addEventListener("resize", ajustarMain);
        window.addEventListener("scroll", ajustarMain);
      }
    })
    .catch((error) => console.error(error));
});
