/* heatmap.static.heatmapScripts.js */

document.addEventListener("DOMContentLoaded", function() {
    // Event listener for the "Update Heatmap" button
    document.getElementById("update-heatmap").addEventListener("click", function() {
        const startDate = document.getElementById("start-date").value;
        const endDate = document.getElementById("end-date").value;

        // Update the heatmap based on the selected date range
        updateHeatmap(startDate, endDate);
    });

    // Fetch current heatmap data and update on page load
});

// Function for updating the heatmap based on the selected date range
function updateHeatmap(startDate, endDate) {
    // Fetch updated heatmap data using the selected date range
    fetch(`/update_heatmap_data?start_date=${startDate}&end_date=${endDate}`)
        .then(response => response.json())
        .then(data => {
            // Update the heatmap using Plotly
            const heatmapContainer = document.getElementById("chart-div");
            heatmapContainer.innerHTML = data.heatmap
        })
        .catch(error => console.error("Error:", error));
}

