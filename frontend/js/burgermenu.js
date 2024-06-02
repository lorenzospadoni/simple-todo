const burger_menu = document.getElementById('burgermenu');

function toggleBurgered() {
    if (burger_menu.classList.contains("burgered") === true) {
        burger_menu.classList.remove("burgered");
    } else if (burger_menu.classList.contains("burgered") === false) {
        burger_menu.classList.add("burgered");
    } else {
        throw new Error('Could not remove class .burgered from element with #burgermenu id');
    }
}

burger_menu.onclick = () => { toggleBurgered(); }
