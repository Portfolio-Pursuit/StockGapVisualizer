/* scripts.js */

document.addEventListener("DOMContentLoaded", function() {
    const chartForm = document.getElementById("chart-form");

    chartForm.addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent default form submission

        // Fetch current price and update the page
        getCurrentPrice();

        // Disable the Generate Chart button and show loading indicator
        document.getElementById("generate_button").disabled = true;
        document.getElementById("loading_indicator").classList.remove("hidden");

        // Add animation class to other fields
        const inputContainers = document.querySelectorAll(".input-container");
        inputContainers.forEach(container => {
            container.classList.add("animated");
        });

        // Remove animation class after a delay
        setTimeout(() => {
            inputContainers.forEach(container => {
                container.classList.remove("animated");
            });
        }, 500);
    });

    // Fetch current price and update slider value on page load
    getCurrentPrice();
});


// Function for fetching current price
function getCurrentPrice() {
    var symbol = document.getElementById("symbol").value;

    fetch(`/get_current_price?symbol=${symbol}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("current_price").innerText = `Current Price: $${data.current_price}`;
            document.getElementById("target_price").max = data.current_price * 10;
            document.getElementById("target_price").value = data.current_price; // Set target price as current value
            updateSliderValue(data.current_price);
            checkTargetPrice(data.current_price);
            document.getElementById("current_price_container").classList.remove("hidden");
        })
        .catch(error => console.error('Error:', error));
}

// Function for updating slider value
function updateSliderValue(value) {
    document.getElementById("slider_value").textContent = value;
    document.getElementById("slider_value").textContent = value;
}

// Event listener for the Generate Chart button
document.getElementById("generate_button").addEventListener("click", function() {
    getCurrentPrice();
    // Disable the Generate Chart button and show loading indicator
    document.getElementById("generate_button").disabled = true;
    document.getElementById("loading_indicator").classList.remove("hidden");

    // Add animation class to other fields
    const inputContainers = document.querySelectorAll(".input-container");
    inputContainers.forEach(container => {
        container.classList.add("animated");
    });

    // Remove animation class after a delay
    setTimeout(() => {
        inputContainers.forEach(container => {
            container.classList.remove("animated");
        });
    }, 500);
});

