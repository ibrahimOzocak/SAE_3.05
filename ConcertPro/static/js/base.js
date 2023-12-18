function deroulant(){
    const b = document.querySelector(".deroulant");
    const a = document.querySelector(".nav");
    const c = document.querySelector(".main");
    a.classList.toggle('mobile-menu');
    a.classList.toggle('flex');
    b.classList.toggle('animation');
    b.classList.toggle('animationr');
    c.classList.toggle('cacher');
}


function toggleContainerClass(){
    // $("#menu").toggleClass("active");
    var container = document.querySelector("#menu");
    var menu = document.querySelector(".menu-link");
    if (container) {
      container.classList.toggle("active");
      menu.classList.toggle("active");
    }
}