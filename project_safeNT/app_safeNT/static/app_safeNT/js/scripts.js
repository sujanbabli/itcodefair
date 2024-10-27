// script.js

// Optional: Add any JavaScript functionality you need

document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".btn");
    buttons.forEach(button => {
        button.addEventListener("click", function () {
            alert("Button clicked!");
        });
    });
});
