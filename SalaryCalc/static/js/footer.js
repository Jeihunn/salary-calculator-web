(() => {
  let navMenu = document.querySelector(".main-menu nav");
  let openNavMenu = document.querySelector(".open-nav-menu");
  let closeNavBtn = document.querySelector(".close-nav-btn");
  let overlay = document.querySelector(".overlay");
  let mediaSize = 992;
  let mySubmenus = navMenu.querySelectorAll(".submenu");
  let plusIcon = document.createElement("i");

  plusIcon.classList.add("plus");
  mySubmenus.forEach(function (subMenu) {
    let mySubParent = subMenu.previousElementSibling;
    mySubParent.appendChild(plusIcon.cloneNode(true));
  });

  openNavMenu.addEventListener("click", toggleMenu);
  closeNavBtn.addEventListener("click", toggleMenu);
  overlay.addEventListener("click", toggleMenu);

  function toggleMenu() {
    navMenu.classList.toggle("open");
    overlay.classList.toggle("active");
    if (navMenu.querySelector(".menu-has-child-item.active")) {
      navMenu
        .querySelector(".menu-has-child-item.active .submenu")
        .removeAttribute("style");
      navMenu
        .querySelector(".menu-has-child-item.active")
        .classList.remove("active");
    }
  }

  navMenu.addEventListener("click", function (e) {
    if (
      e.target.hasAttribute("data-toggle") &&
      window.innerWidth <= mediaSize
    ) {
      let menuHasChildItem = e.target.parentElement;
      if (menuHasChildItem.classList.contains("active")) {
        collapseMenu();
      } else {
        if (navMenu.querySelector(".menu-has-child-item.active")) {
          collapseMenu();
        }
        menuHasChildItem.classList.add("active");
        let submenu = menuHasChildItem.querySelector(".submenu");
        submenu.style.maxHeight = submenu.scrollHeight + "px";
      }
    }
  });

  function collapseMenu() {
    navMenu
      .querySelector(".menu-has-child-item.active .submenu")
      .removeAttribute("style");
    navMenu
      .querySelector(".menu-has-child-item.active")
      .classList.remove("active");
  }
})();
