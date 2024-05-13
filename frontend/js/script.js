testitem = document.getElementById('testitem');

function dragItem( htmlelement ) {
    htmlelement.style.position = absolute;
    htmlelement.style.top = 0;
}

function myHandler( event ) {
    function dragItem( htmlelement, positionX, positionY ) {
        htmlelement.style.position = "absolute";
        htmlelement.style.bottom = positionY;
        htmlelement.style.left = positionX;
    }
    dragItem(event.target, event.clientX, event.clientY);
}

/* myitems = document.getElementsByClassName("list_item");
for (let i = 0; i < myitems.length; i++) {
    let current_element = myitems[i];
    document.addEventListener("click", myHandler)
} */