/* papertrades.static.papertrades.js */

document.addEventListener("DOMContentLoaded", function() {
    const showPopupButton = document.getElementById("showPopupButton");
    const popupContainer = document.getElementById("popupContainer");

    showPopupButton.addEventListener("click", () => {
        popupContainer.style.display = "block"; // Show the popup
    });

    // Close the popup when the user clicks outside of it
    popupContainer.addEventListener("click", (event) => {
        if (event.target === popupContainer) {
            popupContainer.style.display = "none"; // Hide the popup
        }
    });
});
