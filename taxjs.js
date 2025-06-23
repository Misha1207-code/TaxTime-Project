// taxjs.js
window.addEventListener("scroll", () => {
  const header = document.querySelector("header");
  if (window.scrollY > 50) {
    header.classList.add("shadow-md");
  } else {
    header.classList.remove("shadow-md");
  }
});
