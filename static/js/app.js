document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("form[data-confirma]").forEach((form) => {
    form.addEventListener("submit", (evento) => {
      if (!window.confirm(form.dataset.confirma)) {
        evento.preventDefault();
      }
    });
  });
});