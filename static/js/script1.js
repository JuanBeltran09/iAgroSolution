document.getElementById("inicio").addEventListener("click", function() {
    document.getElementById("contenido").innerHTML=
    "<h2>¡Bienvenido!</h2><p> Descubre la increible biodiversidad de nuestros departamentos.</p>";
});

document.getElementById("sobre").addEventListener("click", function(){
    document.getElementById("contenido").innerHTML="<h2>categoria</h2><p>Conoce nuestra fauna y ecosistemas</p>";
});

document.getElementById("contacto").addEventListener("click",function(){
    document.getElementById("contenido").innerHTML = "<h2>contacto</h2><p>Puedes contactarnos en info@.com</p>";
});

let slideIndex = 0;

function showSlide(index) {
    const slides = document.querySelectorAll(".slide");
    if (index >= slides.length){
        slideIndex = 0;
    } else if (index < 0) {
        slideIndex = slides.length -1;
    }
    for (let i= 0; i < slide.length; i++) {
        slides[i].style.display = "none";
    }
    slides[slideIndex].style.display = "block";
}

function nextSlide(){
    slideIndex++;
    showSlide(slideIndex);
}

document.addEventListener('DOMContentLoaded', function() {

    const myCarousel = document.getElementById('carouselExample');
    const carousel = new bootstrap.Carousel(myCarousel, {
        interval: 3000,
        wrap: true
    });

    myCarousel.addEventListener('slide.bs.carousel', function(event) {
        console.log('Slide event:', event);
    });
});