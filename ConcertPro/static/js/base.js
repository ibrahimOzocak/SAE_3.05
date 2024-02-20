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
    var fermer = document.querySelector(".menu-close");
    if (container) {
      container.classList.toggle("active");
      fermer.classList.toggle("cacher");
    }
}

document.addEventListener('click', function(event) {
   if (!event.target.closest('.menu-link') && !event.target.closest('.menu-close') && !event.target.closest('.menu')) {
      if(document.querySelector("#menu").classList.contains("active")){
        toggleContainerClass();
      }
   }
});

document.addEventListener('DOMContentLoaded', () => {
  var header = document.querySelector("#header");
  var lastScrollValue = 0;

  document.addEventListener('scroll', () => {
     var top = document.documentElement.scrollTop;
     if (lastScrollValue < top) {
        header.classList.add("hidden");
     } else {
        header.classList.remove("hidden");
     }
     lastScrollValue = top;
  });
});
