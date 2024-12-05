document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM fully loaded. JavaScript is running.");

    const toggleButton = document.getElementById("themeToggleButton");
    if (toggleButton) {
        // Remove any existing click listeners (if they exist)
        toggleButton.replaceWith(toggleButton.cloneNode(true));
        const newToggleButton = document.getElementById("themeToggleButton");

        // Attach a fresh event listener
        newToggleButton.addEventListener("click", function () {
            console.log("Button clicked! Toggling theme.");
            document.body.classList.toggle("dark-theme");
        });
    } else {
        console.error("Button with ID 'themeToggleButton' not found.");
    }
});
