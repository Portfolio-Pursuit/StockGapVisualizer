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
  });
  