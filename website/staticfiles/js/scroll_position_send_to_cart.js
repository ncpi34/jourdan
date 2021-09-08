document.addEventListener("DOMContentLoaded", () => {
    let scrollpos = localStorage.getItem('scrollpos');
    if (scrollpos) window.scrollTo(0, parseInt(scrollpos));

    // quantities form max
    let quantities = document.querySelectorAll('.product_quantities')
    let quantities_display = document.querySelectorAll('.quantity_val')
    if(quantities &&  quantities_display){
        for (let i=0; i< quantities.length; i++) {
            quantities_display[i].max = quantities[i].innerHTML
        }
    }

});

window.onbeforeunload = () => {
    localStorage.setItem('scrollpos', window.scrollY.toString());
};
