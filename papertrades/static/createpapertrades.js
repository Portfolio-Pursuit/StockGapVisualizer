/* papertrades.static.createpapertrades.js */

document.addEventListener("DOMContentLoaded", function() {
    $(function() {        
        // Initialize the autocomplete widget
        $("#asset").autocomplete({
            source: sp500, // Provide the list of assets as a data source
            minLength: 1, // Minimum characters before showing suggestions
            select: function(event, ui) {
                // Prevent the default behavior (form submission)
                event.preventDefault();

                // Set the selected value in the input field
                $(this).val(ui.item.label);

                var selectedAsset = ui.item.label;
                updateUIForStockPrice(selectedAsset);
            }
        });

        function updateUIForStockPrice(selectedAsset) {
            getStockPrice(selectedAsset, function(stockPrice) {
                // Check if stockPrice is a valid number
                if (!isNaN(parseFloat(stockPrice)) && isFinite(stockPrice)) {
                    // Update the entry_price input field with the valid number
                    $("#entry_price").prop("type", "number"); // Change the input type to number
                    $("#entry_price").val(parseFloat(stockPrice));
                } else {
                    // Set the input type to text and display 'Unknown' in the entry_price input field
                    $("#entry_price").prop("type", "text");
                    $("#entry_price").val('Unknown');
                }
            });
        }

        function getStockPrice(asset, callback) {
            var stockPrice = 0;

            fetch(`/chart/get_current_price?symbol=${asset}`)
                .then(response => response.json())
                .then(data => {
                    stockPrice = data.current_price;
                    callback(stockPrice); // Call the callback function with the stock price
                })
                .catch(error => console.error('Error:', error));
        }

        $("#entry_price").val("");

        $("#asset").on("change", function() {
            var selectedAsset = $(this).val();
            updateUIForStockPrice(selectedAsset);
        });
    });
});