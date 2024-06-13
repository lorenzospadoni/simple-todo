const burger_menu = document.getElementById('burgermenu');
const aside = document.querySelector('aside');

function toggleBurgered() {
    if (burger_menu.classList.contains("burgered") === true) {
        burger_menu.classList.remove("burgered");
        aside.classList.remove('aside-shown');
        aside.classList.add('aside-hidden');


        
    } else if (burger_menu.classList.contains("burgered") === false) {
        burger_menu.classList.add("burgered");
        aside.classList.add('aside-shown');
        aside.classList.remove('aside-hidden');

    } else {
        throw new Error('Could not remove class .burgered from element with #burgermenu id');
    }
}

burger_menu.onclick = () => { toggleBurgered(); }
aside.classList.add('aside-hidden');
