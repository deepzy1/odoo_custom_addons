document.addEventListener("DOMContentLoaded", function () {
    console.log("Custom Slideshow Page Loaded");

    const slides = document.querySelectorAll(".slide");
    const prevButton = document.getElementById("prevButton");
    const nextButton = document.getElementById("nextButton");
    let currentIndex = 0;

    function showSlide(index) {
        // Hide all slides
        slides.forEach(slide => slide.classList.remove("active"));

        // Show the slide at the given index
        slides[index].classList.add("active");
    }

    function showNextSlide() {
        currentIndex = (currentIndex + 1) % slides.length; // Loop back to the first slide
        showSlide(currentIndex);
    }

    function showPrevSlide() {
        currentIndex = (currentIndex - 1 + slides.length) % slides.length; // Loop to the last slide
        showSlide(currentIndex);
    }

    // Event listeners for arrow buttons
    nextButton.addEventListener("click", showNextSlide);
    prevButton.addEventListener("click", showPrevSlide);

    // Auto-play the slideshow
    setInterval(showNextSlide, 3000); // Change slide every 3 seconds
});
