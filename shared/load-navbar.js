document.addEventListener("DOMContentLoaded", () => {
  const placeholder = document.getElementById("navbar-placeholder");

  // 절대 경로로 고정 (루트에서 항상 동일)
  fetch("/shared/navbar.html")
    .then(res => res.text())
    .then(html => {
      placeholder.innerHTML = html;

      // 현재 페이지 경로에 따라 active 클래스 설정
      const links = document.querySelectorAll(".navbar .menu a");
      links.forEach(link => {
        if (window.location.pathname.includes(link.getAttribute("href"))) {
          link.classList.add("active");
        }
      });
    });
});
