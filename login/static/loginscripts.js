/* login.static.loginscripts.js */

document.addEventListener("DOMContentLoaded", function() {
    const showPopupButton = document.getElementById("show-registration");
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

$(document).ready(function () {
    // Submit the registration form via AJAX
    $('#register-form').submit(function (e) {
        e.preventDefault();
        var formData = $(this).serialize();
        $.ajax({
            type: 'POST',
            url: '/login/register',
            data: formData,
            success: function (response) {
                if (response.success) {
                    // Registration was successful, redirect or perform other actions
                    window.location.href = '/dashboard';
                } else if (response.error) {
                    // Display registration error message
                    $('#register-error').text(response.error);
                }
            },
            error: function () {
                // Handle AJAX error
                $('#register-error').text('An error occurred during registration.');
            }
        });
    });
});
