let map;
let markers = [];
let lastKnownSpot = null;
let isManualSearch = false; // Prevents GPS from "snapping back" during search

window.onload = () => {
    // 1. Initialize Map
    map = L.map('map').setView([20.59, 78.96], 5);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // 2. Start Watching GPS with High Accuracy
    map.locate({
        setView: true, 
        maxZoom: 14, 
        watch: true, 
        enableHighAccuracy: true
    });

    // 3. Handle GPS Location Found
    map.on('locationfound', (e) => {
        const userLat = e.latlng.lat;
        const userLng = e.latlng.lng;
        
        // Only move the map automatically if the user isn't searching somewhere else
        if (!isManualSearch) {
            map.setView(e.latlng, map.getZoom());
        }

        // Run Auto-Detect Logic
        checkAutomaticStatus(userLat, userLng);
        
        // Fetch parking based on where the MAP is currently looking
        const center = map.getCenter();
        fetchParking(center.lat, center.lng);
    });

    map.on('locationerror', () => {
        console.log("GPS blocked. Defaulting to manual mode.");
        fetchParking(26.14, 91.64); // Guwahati fallback
    });
};

/** * FIX: Manual Search Function
 */
async function manualSearch() {
    const query = document.getElementById('location-input').value;
    if (!query) return;

    isManualSearch = true; // Tell the GPS "don't pull me back"

    try {
        const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${query}`);
        const data = await res.json();

        if (data.length > 0) {
            const lat = parseFloat(data[0].lat);
            const lon = parseFloat(data[0].lon);

            map.setView([lat, lon], 13);
            
            // Marker for the searched spot
            L.marker([lat, lon]).addTo(map)
                .bindPopup(`<b>Searching: ${query}</b>`)
                .openPopup();

            fetchParking(lat, lon);
        } else {
            alert("Location not found. Try a specific city name.");
        }
    } catch (e) {
        console.error("Geocoding failed:", e);
    }
}

/**
 * AUTO-DETECTION: The "No-Button" Logic
 */
function checkAutomaticStatus(uLat, uLng) {
    if (!markers.length) return;

    markers.forEach(m => {
        const spotLat = m.getLatLng().lat;
        const spotLng = m.getLatLng().lng;
        const spotName = m.options.title;

        // Calculate distance in meters
        const distance = map.distance([uLat, uLng], [spotLat, spotLng]);

        // Auto-Park: Within 30 meters
        if (distance < 30 && lastKnownSpot !== spotName) {
            console.log("AUTO-PARK triggered at " + spotName);
            reportActivity(spotName, 'park');
            lastKnownSpot = spotName;
            showNotification(`You parked at ${spotName}!`);
        }

        // Auto-Leave: Previously parked here, now > 100 meters away
        if (lastKnownSpot === spotName && distance > 100) {
            console.log("AUTO-LEAVE triggered for " + spotName);
            reportActivity(spotName, 'leave');
            lastKnownSpot = null;
            showNotification(`You left ${spotName}. Happy driving!`);
        }
    });
}

/**
 * CORE: Fetch Data
 */
async function fetchParking(lat, lng) {
    try {
        const res = await fetch('https://smart-parking-system-3.onrender.com/predict', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ latitude: lat, longitude: lng })
        });
        const data = await res.json();

        markers.forEach(m => map.removeLayer(m));
        markers = [];

        data.spots.forEach(spot => {
            const fused = Math.round((spot.live_count * 0.8) + (spot.ml_count * 0.2));
            const color = fused > 10 ? '#27ae60' : '#e74c3c';

            const marker = L.circleMarker([spot.lat, spot.lng], {
                radius: 15,
                fillColor: color,
                color: '#fff',
                weight: 2,
                fillOpacity: 0.8,
                className: 'fused-pulse',
                title: spot.name // Used for tracking logic
            }).addTo(map);

            marker.bindPopup(`
                <div style="text-align:center;">
                    <strong>${spot.name}</strong><br>
                    <small>${spot.distance} km away</small>
                    <h2 style="color:${color}; margin:5px 0;">${fused}</h2>
                    <p style="font-size:10px;">Autodetect Enabled 📡</p>
                </div>
            `);
            markers.push(marker);
        });
    } catch (err) {
        console.error("Backend offline.");
    }
}

/**
 * UTILS: API Reporting & UI Notifications
 */
async function reportActivity(name, action) {
    await fetch('https://smart-parking-system-3.onrender.com/update_activity', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ name: name, action: action })
    });
}

function showNotification(msg) {
    // Simple alert or you can create a custom HTML div notification
    console.log("NOTIFICATION: " + msg);

}
