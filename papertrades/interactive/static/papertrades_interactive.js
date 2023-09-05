/* papertrades.interactive.static.papertrades_interactive.js */

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

function removePaperTrade(tradeId) {
    // Make an AJAX request to the remove_paper_trade endpoint
    fetch(`/papertrading/interactive/remove/${tradeId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.status === 200) {
            // If the removal was successful, remove the row from the table
            const rowToRemove = document.getElementById(`papertrade-data-row-${tradeId}`);
            if (rowToRemove) {
                rowToRemove.remove();
            }
        } else {
            console.error('Failed to remove paper trade');
        }
    })
    .catch(error => {
        console.error('Error while removing paper trade', error);
    });
}