document.addEventListener("DOMContentLoaded", () => {
  const vitrine = document.querySelector(".vitrine");
  const reduzir = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  
  // Controle de Animação do Carrossel (IHC: Autonomia do usuário)
  if (vitrine && !reduzir) {
    let atual = 0;
    let autoPlay;
    const slides = vitrine.querySelectorAll(".slide");

    const iniciarCarrossel = () => {
      autoPlay = setInterval(() => {
        if (slides.length < 2) return;
        atual = (atual + 1) % slides.length;
        vitrine.scrollTo({ left: slides[atual].offsetLeft, behavior: "smooth" });
      }, 5000);
    };

    if (slides.length >= 2) {
      iniciarCarrossel();
      // Pausa a rolagem automática quando o usuário está interagindo
      vitrine.addEventListener("mouseenter", () => clearInterval(autoPlay));
      vitrine.addEventListener("mouseleave", iniciarCarrossel);
      vitrine.addEventListener("focusin", () => clearInterval(autoPlay));
      vitrine.addEventListener("focusout", iniciarCarrossel);
    }
  }

  // Prevenção de Erros em ações destrutivas
  document.querySelectorAll("form[data-confirma]").forEach((form) => {
    form.addEventListener("submit", (evento) => {
      if (!window.confirm(form.dataset.confirma)) {
        evento.preventDefault();
      }
    });
  });
});