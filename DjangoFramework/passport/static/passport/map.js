// Initialize Leaflet map (temporary center, zoom 2)
const map = L.map('map').setView([20, 0], 2);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);
var allMarkers = L.featureGroup().addTo(map);

// Function to get lat and long from OpenStreetMap Nominatim
async function geocode(city, country) {
    const query = encodeURIComponent(`${city}, ${country}`);
    const url = `https://nominatim.openstreetmap.org/search?q=${query}&format=json&limit=1`;
    console.log(url);
    try {
        const response = await fetch(url);
        const data = await response.json();
        if (data.length > 0) {
            return [parseFloat(data[0].lat), parseFloat(data[0].lon)];
        }
    } catch (err) {
        console.error("Geocoding error:", err);
    }
    return null;
}

async function addLocation(city, country,label) {
    geocode(city, country).then(coords => {
        if (coords) {
            var marker = L.marker(coords)
                .addTo(map)
                .bindPopup(`<b>${city}(${country})</b><br>${label}`)
                .openPopup();
            allMarkers.addLayer(marker);
             map.fitBounds(allMarkers.getBounds(), { padding: [50, 50] });
        } else {
            console.warn("Could not find location");
        }
    });
}

