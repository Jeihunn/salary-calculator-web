const activeMenuItems = document.querySelectorAll(
  ".main-menu nav ul .menu-has-child-item ul li a.active"
);

activeMenuItems.forEach((activeMenuItem) => {
  const parentElement = activeMenuItem
    .closest(".menu-has-child-item")
    .querySelector("a");
  parentElement.style.color = "var(--secondary)";
});
