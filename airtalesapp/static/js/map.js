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

    // Add markers for each entry that has location data
    if (typeof entries !== 'undefined' && entries.length > 0) {
        entries.forEach(entry => {
            if (entry.latitude && entry.longitude) {
                addMarkerWithPopup(entry.latitude, entry.longitude, `
                    <b>${entry.date}</b><br>
                    ${entry.entry}<br>
                    <button onclick="toggleLike(${entry.id})" id="like-button-${entry.id}" class="like-button ${authenticated ? "" : "d-none"}">${entry.isLiked ? "Unlike" : "Like"}</button>
                    <p id="login-alert-${entry.id}" class="${authenticated ? "d-none" : ""}">You need to be signed in to like</p>
                    <p>Likes: <span id="like-count-${entry.id}">${entry.likes}</span></p>
                `);
                
            }
        });
    } else {
        console.warn("Entries array is empty.");
    }
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

var map = null;
document.addEventListener("DOMContentLoaded", setupMap);

// for liking and unliking entries on the map

function toggleLike(entryId) {
    if (entryId === undefined) {
        console.error("Cannot toggle like for undefined entry ID");
        return;
    }

    const csrfToken = Cookies.get("csrftoken");
    if (!csrfToken) {
        console.error("Cannot toggle like because the CSRF token cookie not found or inaccessible.");
        return;
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
            const entry = entries.find(entry => entry.id === entryId);

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
                console.error('Error updating like status:', error);
            }
        }
    });
}
