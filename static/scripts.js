/* scripts.js */
document.addEventListener("DOMContentLoaded", function() {
    getCurrentPrice();
});


// Function for fetching current price
function getCurrentPrice() {
    var symbol = document.getElementById("symbol").value;

    fetch(`/get_current_price?symbol=${symbol}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("target_price").max = data.current_price * 10;
            document.getElementById("target_price").value = data.current_price; // Set target price as current value
            updateSliderValue(data.current_price);
            // checkTargetPrice(data.current_price);
            // document.getElementById("current_price_container").classList.remove("hidden");
        })
        .catch(error => console.error('Error:', error));
}

// Function for updating slider value
function updateSliderValue(value) {
    document.getElementById("slider_value").textContent = value;
    document.getElementById("slider_value").textContent = value;
}