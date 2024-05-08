const userMenu = document.querySelector(".user-link");
const sidebar = document.querySelector(".sidebar");

userMenu.addEventListener("click", menuToggle);
sidebar.addEventListener("mouseout", menuToggle2);




function menuToggle2() {
    if (!document.querySelector(".sidebar:hover")) {
        const togglemenu = document.querySelector('.user-menu');
        togglemenu.classList.remove('active');
    }
}

function menuToggle() {
    const togglemenu = document.querySelector('.user-menu');
    if (document.querySelector(".sidebar")) {
        togglemenu.classList.toggle('active');
    } else {

    }
}