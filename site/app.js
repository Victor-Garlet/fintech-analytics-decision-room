const filterButtons = document.querySelectorAll(".filter");
const evidenceCards = document.querySelectorAll(".evidence-card");

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const selected = button.dataset.filter;

    filterButtons.forEach((item) => item.classList.toggle("is-active", item === button));
    evidenceCards.forEach((card) => {
      const visible = selected === "all" || card.dataset.kind === selected;
      card.classList.toggle("is-muted", !visible);
    });
  });
});
