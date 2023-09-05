/* papertrades.interactive.static.createpapertrades.js */

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
                    $("#entry_price").val("Not Valid Ticker"); 
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

function createPaperTrade() {
    // Get form values
    const asset = document.getElementById('asset').value;
    const direction = document.getElementById('direction').value;
    const quantity = document.getElementById('quantity').value;
    const entryPrice = document.getElementById('entry_price').value;

    // Make an AJAX request to the create_paper_trade endpoint
    fetch('/papertrading/interactive/new', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            asset,
            direction,
            quantity,
            entryPrice,
        }),
    })
    .then(response => {
        if (response.status === 200) {
            return response.json();
        } else if (response.status == 400) {
            return response.text().then(errorMessage => {
                console.error(errorMessage);
                const errorElement = document.getElementById('error-message');
                errorElement.textContent = errorMessage;
                throw new Error('Failed to create paper trade');
            });
        } else {
            console.error('Failed to create paper trade');
            throw new Error('Failed to create paper trade');
        }
    })
    .then(data => {
        const totalCurrencyElement = document.querySelector('.total-currency');
        totalCurrencyElement.textContent = `Total Currency: ${data.total_currency}`;

        // Update the table with the new paper trade data
        const tableBody = document.querySelector('.papertrades-table tbody');
        const newRow = document.createElement('tr');
        newRow.className = 'papertrade-data-row';
        newRow.id = `papertrade-data-row-${data.tradeId}`;
        newRow.innerHTML = `
            <td>${data.tradeId}</td>
            <td>${asset}</td>
            <td>${direction}</td>
            <td>${quantity}</td>
            <td>$${entryPrice}</td>
            <td>${data.timestamp}</td>
            <td id="price-change-${data.tradeId}">Unknown</td>
            <td id="market-value-${data.tradeId}">Unknown</td>
            <td id="cost-basis-${data.tradeId}">Unknown</td>
            <td id="gain-loss-${data.tradeId}">Unknown</td>
            <td id="current-price-${data.tradeId}">Unknown</td>
            <td>
                <button type="button" class="remove-button" onclick="removePaperTrade(${data.tradeId})">X</button>
            </td>
        `;
        tableBody.appendChild(newRow);

        // Clear the form inputs
        document.getElementById('asset').value = '';
        document.getElementById('direction').value = 'buy';
        document.getElementById('quantity').value = '';
        document.getElementById('entry_price').value = '';

        updateStockDataForTrade(data.tradeId); // Fetch updated stock data for the trade
    })
    .catch(error => {
        console.error('Error while creating paper trade', error);
    });
}

function updateStockDataForTrade(tradeId) {
    // Make an AJAX request to get updated stock data for the trade
    fetch(`/papertrading/interactive/get_stock_data/${tradeId}`)
        .then(response => response.json())
        .then(data => {
             // Update the current_stock_data object in the HTML template with the fetched data
             currentPriceElem = document.getElementById(`current-price-${tradeId}`);
             document.getElementById(`current-price-${tradeId}`).textContent = data.current_price;
             document.getElementById(`price-change-${tradeId}`).textContent = data.price_change;
             document.getElementById(`market-value-${tradeId}`).textContent = data.market_value;
             document.getElementById(`cost-basis-${tradeId}`).textContent = data.cost_basis;
             document.getElementById(`gain-loss-${tradeId}`).textContent = data.gain_loss;
        })
        .catch(error => console.error('Error:', error));
}