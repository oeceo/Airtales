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

    // Add markers for each entry
    if (typeof entries !== 'undefined' && entries.length > 0) {
        entries.forEach(entry => {
            console.log("Processing entry:", entry);

            if (entry.latitude && entry.longitude) {
                console.log("Adding marker at:", entry.latitude, entry.longitude);
                addMarkerWithPopup(entry.latitude, entry.longitude, `
                    <b>${entry.date}</b><br>
                    ${entry.entry}
                `);
            } else {
                console.warn("Invalid coordinates for entry:", entry);
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