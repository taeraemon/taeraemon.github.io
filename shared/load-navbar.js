document.addEventListener("DOMContentLoaded", () => {
    const placeholder = document.getElementById("navbar-placeholder");
    const currentPath = window.location.pathname;
  
    // 경로에 따라 상대 경로 자동 조절
    let navbarPath = "shared/navbar.html";
    if (currentPath.includes("/blog/") || currentPath.includes("/projects/")) {
      navbarPath = "../shared/navbar.html";
    }
  
    fetch(navbarPath)
      .then(res => res.text())
      .then(html => {
        placeholder.innerHTML = html;
  
        // 현재 페이지 경로에 따라 active 클래스 설정
        const links = document.querySelectorAll(".navbar .menu a");
        links.forEach(link => {
          // 현재 경로가 링크 href를 포함하면 active 붙이기
          if (currentPath.includes(link.getAttribute("href"))) {
            link.classList.add("active");
          }
        });
      });
  });
  