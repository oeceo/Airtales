function setupMap() {
    if (typeof L === 'undefined') {
        console.error("Leaflet library did not load.");
        return;
    }

    console.log("Initializing map...");

    // TODO set coordinates of Glasgow uni
    map = L.map('map').setView([51.505, -0.09], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 12,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Force resize after a short delay
    setTimeout(() => {
        map.invalidateSize();
        console.log("Map has been resized");
    }, 500);
}

function addMarkerWithPopup(lat, long, text) {
    let marker = L.marker([lat, long]).addTo(map);
    marker.bindPopup(text);
}

var map = null;
document.addEventListener("DOMContentLoaded", setupMap);
