document.addEventListener("DOMContentLoaded", () => {
  const placeholder = document.getElementById("navbar-placeholder");

  if (!placeholder) {
    return;
  }

  fetch("/shared/navbar.html")
    .then(res => res.text())
    .then(html => {
      placeholder.innerHTML = html;

      const currentPath = window.location.pathname === "/" ? "/index.html" : window.location.pathname;
      const links = document.querySelectorAll(".navbar .menu a");

      links.forEach(link => {
        const href = link.getAttribute("href");
        if (href === currentPath) {
          link.classList.add("active");
        }
      });
    });
});
