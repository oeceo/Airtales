var map = null;
var authenticated = false;
var entries = [];

function setupMap() {
    if (typeof L === 'undefined') {
        console.error("Leaflet library did not load.");
        return;
    }

    console.log("Initializing map...");

    // Center on Glasgow Uni
    map = L.map('map').setView([55.8721, -4.2886], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 12,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Force resize after a short delay
    setTimeout(() => {
        map.invalidateSize();
        console.log("Map has been resized");
    }, 500);

    const entries = loadEntriesFromServer();
}

function loadEntriesFromServer() {
    // Make an AJAX GET request to get all entries
    $.ajax({    
        url: '/entries/',  // URL to the Django view
        method: 'GET',
        success: function(response) {
            console.log('Entries loaded from server successfully');  
            entries = $.parseJSON(response.entries);      

            let user = document.getElementById("current-user")?.innerText;
            if (!user) {
                console.error("Failed to find user");
            } else {
                user = Number(user)
            }
            authenticated = user !== null;

            entries.forEach(entry => {
                const isSameUser = entry.fields.userID === user;  // Only show report button if it's not the signed-in user's entry
                const liked = entry.fields.liked_by.includes(user);
                const likes = entry.fields.liked_by.length;
                if (entry.fields.latitude && entry.fields.longitude) {
                    addMarkerWithPopup(entry.fields.latitude, entry.fields.longitude, `
                        <b>${entry.fields.date}</b><br>
                        ${entry.fields.entry}<br>
                        <button onclick="toggleLike(${entry.pk})" id="like-button-${entry.pk}" class="like-button ${authenticated ? "" : "d-none"}">${liked ? "Unlike" : "Like"}</button>
                        <p id="login-alert-${entry.pk}" class="${authenticated ? "d-none" : ""}">You need to be signed in to like or report entries</p>
                        <p>Likes: <span id="like-count-${entry.pk}">${likes}</span></p>
                        <p><span id="report-status-${entry.pk}">${entry.fields.isReported ? "This entry has been reported" : ""}</span></p>
                        ${!isSameUser && authenticated && !entry.fields.isReported ? `<button onclick="reportEntry(${entry.pk})" class="report-button" id="report-button-${entry.pk}">Report</button>` : ''}
                    `);
                }
            });
        },
        error: function(error) {
            console.error("Failed to load entries from server:", error.responseJSON);
        }
    });
}


function addMarkerWithPopup(lat, long, text) {
    // create a custom icon for the map pins
    const customIcon = L.icon({
        iconUrl: "/static/images/mapPin.png",  // make this not hard coded but {static wont work for some reason}
        iconSize: [32, 32], 
        iconAnchor: [16, 32], 
        popupAnchor: [0, -32], 
        
    });

    // create the marker with the custom icon
    let marker = L.marker([lat, long], { icon: customIcon }).addTo(map);
    marker.bindPopup(text);
}

// for liking and unliking entries on the map
function toggleLike(entryId) {
    if (entryId === undefined) {
        console.error("Cannot toggle like for undefined entry ID");
        return;
    }

    const csrfToken = getCsrfToken()
    if (!csrfToken) {
        console.error("Cannot toggle like because the CSRF token cookie not found or inaccessible.");
    }

    // Send the AJAX request to update the like status in the backend
    $.ajax({
        url: '/like-entry/' + entryId + "/",  // URL to the Django view
        method: 'POST',
        data: {
            'csrfmiddlewaretoken': csrfToken
        },
        success: function(response) {
            console.log('Like status updated successfully');
            const entry = entries.find(entry => entry.pk === entryId);

            entry.isLiked = response["is_liked"];
            entry.likes = response["likes"]
        
            // Try to get the like elements
            const likeButton = document.getElementById('like-button-' + entryId);
            const likeCount = document.getElementById('like-count-' + entryId);
            
            // Check if the elements exist before trying to access their properties
            if (likeButton) {
                likeButton.textContent = entry.isLiked ? 'Unlike' : 'Like';
            } else {
                console.error("Like button not found for entryId:", entryId);
            }

            if (likeCount) {
                likeCount.innerText = entry.likes;
            } else {
                console.error("Like count not found for entryId:", entryId);
            }

        },
        error: function(error) {
            if (error.status === 403 || error.status === 401) {
                const loginAlert = document.getElementById("login-alert-" + entryId);
                if (loginAlert) {
                    loginAlert.classList.remove("d-none");
                } else {
                    console.error("Login alert not found for entryId:", entryId);
                }
            } else {
                console.error('Error updating like status:', error.responseJSON);
            }
        }
    });
}

function reportEntry(entryId) {
    const csrfToken = getCsrfToken()
    if (!csrfToken) {
        console.error("Cannot report entry because the CSRF token cookie not found or inaccessible.");
    }

    // Make an AJAX POST request to report the entry
    $.ajax({
        url: '/report-entry/' + entryId + "/",  // URL to the Django view
        method: 'POST',
        data: {
            'csrfmiddlewaretoken': csrfToken
        },
        success: function(response) {
            console.log('Entry reported successfully');
            const entry = entries.find(entry => entry.pk === entryId);

            entry.isLiked = response["is_liked"];
            entry.likes = response["likes"]
        
            // Try to get the report elements
            const reportButton = document.getElementById(`report-button-${entryId}`);
            const reportStatus = document.getElementById(`report-status-${entryId}`);
            
            // Check if the element exists before trying to access its properties
            if (reportButton) {
                reportButton.style.display = 'none';
            } else {
                console.error("Report entry button not found for entryId:", entryId);
            }

            if (reportStatus) {
                reportStatus.innerText = "This entry has been reported";
            } else {
                console.error("Failed to find report status element for entry ID ", entryId);
            }
        },
        error: function(error) {
            const reportStatus = document.getElementById(`report-status-${entryId}`);

            if (error.status === 403 || error.status === 401) {
                const loginAlert = document.getElementById("login-alert-" + entryId);
                if (loginAlert) {
                    loginAlert.classList.remove("d-none");
                } else {
                    console.error("Login alert not found for entryId:", entryId);
                }
            } else {
                console.error('Error reporting entry:', error.responseJSON);
                if (reportStatus) {
                    reportStatus.innerText = "Failed to report entry";
                } else {
                    console.error("Failed to find report status element for entry ID ", entryId);
                }
            }
        }
    });
}

function getCsrfToken() {
    const csrfToken = Cookies.get("csrftoken");

    return csrfToken;
}

// For the button on explore page under the map
document.addEventListener('DOMContentLoaded', function() {
    setupMap();
    
    const loginButton = document.getElementById('login-status-btn');

    // Ensure the button exists before manipulating it
    if (loginButton) {
        // Check the authentication status and update the button text
        if (authenticated) {
            loginButton.textContent = 'share your tale today';
        } else {
            loginButton.textContent = 'login/signup to share your tale';
        }

        // If the button is clicked then redirect accordingly
        loginButton.addEventListener('click', function() {
            if (!authenticated) {
                window.location.href = '/login/';  // Redirect to login page if not logged in
            } else {
                window.location.href = '/profile/'
            }
        });
    }
});
