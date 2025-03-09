document.addEventListener("DOMContentLoaded", function () {
    const saveButton = document.getElementById("journal-entry-button");
    const journalForm = document.getElementById("journalForm");

    if (saveButton && journalForm) {
        saveButton.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent immediate form submission
            console.log("Button clicked. Triggering geolocation...");
            getLocation(journalForm); // Pass form to the function
        });
    }
});

function getLocation(form) {
    if (navigator.geolocation) {
        console.log("Geolocation is supported. Requesting location...");
        
        navigator.geolocation.getCurrentPosition(
            function (position) {
                console.log("Location retrieved!");
                console.log("Latitude: " + position.coords.latitude);
                console.log("Longitude: " + position.coords.longitude);

                // Set the coordinates in the form fields
                document.getElementById("latitude").value = position.coords.latitude;
                document.getElementById("longitude").value = position.coords.longitude;

                // Log the form fields to check if they are being set correctly
                console.log("Latitude field value: " + document.getElementById("latitude").value);
                console.log("Longitude field value: " + document.getElementById("longitude").value);

                // Submit the form after setting coordinates
                form.submit();
            },
            function (error) {
                console.error("Geolocation error: " + error.message);
                alert("Failed to get location: " + error.message);

                // Set empty values if location retrieval fails
                document.getElementById("latitude").value = '';
                document.getElementById("longitude").value = '';

                // Submit the form regardless of geolocation failure (optional)
                form.submit();
            }
        );
    } else {
        alert("Geolocation is not supported by this browser.");

        // Set empty values if geolocation is unsupported
        document.getElementById("latitude").value = '';
        document.getElementById("longitude").value = '';

        // Still submit the form
        form.submit();
    }
}