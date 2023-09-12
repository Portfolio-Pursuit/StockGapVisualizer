document.addEventListener("DOMContentLoaded", function () {
    // Initialize the autocomplete widget
    $(function () {
      $("#newStockSymbol").autocomplete({
        source: sp500, // Provide the list of assets as a data source
        minLength: 1, // Minimum characters before showing suggestions
        select: function (event, ui) {
          // Prevent the default behavior (form submission)
          event.preventDefault();
  
          // Set the selected value in the input field
          $(this).val(ui.item.label);
        },
      });
    });
  
    // Attach event listeners to the "Remove" buttons for each stock
    $(document).on("click", ".removeButton", function () {
      const symbol = $(this).data("symbol");
  
      if (symbol) {
        // Send an AJAX request to remove the stock
        $.ajax({
          url: "/watchlist/delete_stock",
          method: "POST",
          data: { stockSymbol: symbol },
          success: function () {
            // Remove the stock's list item from the page
            $(`li[data-symbol="${symbol}"]`).remove();
          },
          error: function (xhr, status, error) {
            console.error(error);
          },
        });
      }
    });
  });
  