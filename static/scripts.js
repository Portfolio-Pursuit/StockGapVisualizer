/* scripts.js */
document.addEventListener("DOMContentLoaded", function() {
    // Event listener for the "Update Heatmap" button
    document.getElementById("update-heatmap").addEventListener("click", function() {
        const startDate = document.getElementById("start-date").value;
        const endDate = document.getElementById("end-date").value;

        // Update the heatmap based on the selected date range
        updateHeatmap(startDate, endDate);
    });

    // Fetch current price and update slider value on page load
    getHeatmapData();
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

// Function for fetching heatmap data
function getHeatmapData() {
    // Fetch heatmap data using an API endpoint (implement in your Flask app)
    fetch("/get_heatmap_data")
        .then(response => response.json())
        .then(data => {
            // Create the heatmap using Plotly
            const heatmap = createHeatmap(data);

            // Render the heatmap in the specified container
            const heatmapContainer = document.getElementById("heatmap-div");
            Plotly.newPlot(heatmapContainer, heatmap);
        })
        .catch(error => console.error("Error:", error));
}

// Function for updating the heatmap based on the selected date range
function updateHeatmap(startDate, endDate) {
    // Fetch updated heatmap data using the selected date range
    fetch(`/update_heatmap_data?start_date=${startDate}&end_date=${endDate}`)
        .then(response => response.json())
        .then(data => {
            // Update the heatmap using Plotly
            const heatmapContainer = document.getElementById("heatmap-div");
            Plotly.react(heatmapContainer, createHeatmap(data));
        })
        .catch(error => console.error("Error:", error));
}

// Function for creating the heatmap using Plotly
function createHeatmap(data) {
    // Customize the heatmap creation using Plotly
    // You'll need to structure your data appropriately for the heatmap
    const heatmap = {
        // ... Plotly heatmap configuration ...
    };
    return heatmap;
}
