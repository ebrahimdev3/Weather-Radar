const BACKEND_BASE_URL = "https://weather-radar-cx6x.onrender.com";

const map = L.map('map', {
    zoomControl: false 
}).setView([12.63, -8.00], 5);

L.control.zoom({
    position: 'bottomleft'
}).addTo(map);

L.tileLayer('https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
    attribution: '&copy; Google Maps',
    maxZoom: 20,
    useCache: true,         
    crossOrigin: true,      
    cacheMaxAge: 604800000  
}).addTo(map);

L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_only_labels/{z}/{x}/{y}{r}.png', {
    subdomains: 'abcd',
    maxZoom: 20,
    opacity: 0.85,
    useCache: true,
    crossOrigin: true,
    cacheMaxAge: 604800000
}).addTo(map);

let currentWeatherDataLayer;
let animationInterval = null;
let currentOpacity = 0.75; 
let currentLayerType = 'temp';
let isAnimating = false; 

const legendConfigs = {
    temp: { 
        title: "🌡️ Thermal Tracks & Contours", 
        gradient: "linear-gradient(to right, #002051, #00a896, #ffff3f, #ff7b00, #ff0000)", 
        min: "-20°C (Polar)", 
        mid: "15°C (Mild)", 
        max: "45°C (Extreme Heat)" 
    },
    precipitation: { 
        title: "🌧️ Heavy Rain Radar & Storm Cells", 
        gradient: "linear-gradient(to right, rgba(255,255,255,0), #00f5d4, #00bbf9, #00f, #7000ff)", 
        min: "Drizzle", 
        mid: "Moderate", 
        max: "Torrential / Hail" 
    },
    wind: { 
        title: "💨 Airflow Circulation & Isobars", 
        gradient: "linear-gradient(to right, #1a1a1a, #0ad63d, #00f5d4, #ff007f, #ffff00)", 
        min: "Calm Breeze", 
        mid: "Gale (15 m/s)", 
        max: "Storm Force (35 m/s)" 
    }
};

const sidebar = document.getElementById('sidebar-control');
document.getElementById('menu-toggle').addEventListener('click', () => sidebar.classList.add('active'));
document.getElementById('close-sidebar').addEventListener('click', () => sidebar.classList.remove('active'));

function updateWeatherLayer(layerType) {
    currentLayerType = layerType;
    if (currentWeatherDataLayer) {
        map.removeLayer(currentWeatherDataLayer);
    }

    let layerName = 'temp_new';
    if (layerType === 'precipitation') layerName = 'precipitation_new';
    if (layerType === 'wind') layerName = 'wind_new';

    currentWeatherDataLayer = L.tileLayer(`${BACKEND_BASE_URL}/api/tiles/${layerName}/{z}/{x}/{y}.png`, {
        opacity: currentOpacity,
        zIndex: 500,
        useCache: true,        
        crossOrigin: true,
        cacheMaxAge: 1800000   
    });

    currentWeatherDataLayer.on('tileload', function(event) {
        event.tile.classList.add('high-contrast-radar');
    });

    currentWeatherDataLayer.addTo(map);

    const config = legendConfigs[layerType];
    document.getElementById('legend-title').innerText = config.title;
    document.querySelector('.legend-bar').style.background = config.gradient;
    const labels = document.querySelectorAll('.legend-labels span');
    labels[0].innerText = config.min;
    labels[1].innerText = config.mid;
    labels[2].innerText = config.max;
}

function startRadarAnimation() {
    if (animationInterval) clearInterval(animationInterval);
    let pulseUp = false;
    animationInterval = setInterval(() => {
        if (!currentWeatherDataLayer) return;
        let targetOpacity = pulseUp ? currentOpacity : currentOpacity - 0.15;
        currentWeatherDataLayer.setOpacity(Math.max(0.30, targetOpacity));
        pulseUp = !pulseUp;
    }, 900);
}

function stopRadarAnimation() {
    if (animationInterval) {
        clearInterval(animationInterval);
        animationInterval = null;
    }
    if (currentWeatherDataLayer) currentWeatherDataLayer.setOpacity(currentOpacity);
}

document.getElementById('radar-toggle').addEventListener('click', (e) => {
    const btn = e.target;
    if (!isAnimating) {
        startRadarAnimation();
        btn.innerText = "⏸ Freeze Loop";
        btn.classList.remove('btn-stopped');
        btn.classList.add('btn-playing');
        isAnimating = true;
    } else {
        stopRadarAnimation();
        btn.innerText = "▶ Live Stream";
        btn.classList.remove('btn-playing');
        btn.classList.add('btn-stopped');
        isAnimating = false;
    }
});

updateWeatherLayer('temp');

document.querySelectorAll('input[name="weather-layer"]').forEach(radio => {
    radio.addEventListener('change', (e) => updateWeatherLayer(e.target.value));
});

document.getElementById('opacity-slider').addEventListener('input', (e) => {
    currentOpacity = e.target.value / 100;
    document.getElementById('opacity-val').innerText = `${e.target.value}%`;
    if (currentWeatherDataLayer && !isAnimating) {
        currentWeatherDataLayer.setOpacity(currentOpacity);
    }
});

async function fetchAndShowWeather(lat, lon, cityName = null) {
    const loadingPopup = L.popup().setLatLng([lat, lon]).setContent("Syncing data...").openOn(map);

    try {
        const response = await fetch(`${BACKEND_BASE_URL}/api/weather?lat=${lat}&lon=${lon}`);
        if (!response.ok) throw new Error();
        const data = await response.json();

        loadingPopup.setContent(`
            <div class="weather-popup">
                <h3>📍 ${cityName || data.city}</h3>
                <p><strong>🌡️ Temperature:</strong> ${data.temperature}°C</p>
                <p><strong>🌤️ Condition:</strong> ${data.condition}</p>
                <p><strong>💧 Humidity:</strong> ${data.humidity}%</p>
                <p><strong>💨 Wind Speed:</strong> ${data.wind_speed} m/s</p>
            </div>
        `);
        map.setView([lat, lon], 6);
    } catch {
        loadingPopup.setContent("Connection broken.");
    }
}

map.on('click', (e) => fetchAndShowWeather(e.latlng.lat, e.latlng.lng));

async function searchCity() {
    const cityInput = document.getElementById('city-input');
    const city = cityInput.value.trim();
    if (!city) return;

    cityInput.placeholder = "Searching...";
    
    try {
        const response = await fetch(`${BACKEND_BASE_URL}/api/search?q=${encodeURIComponent(city)}`);
        if (!response.ok) {
            cityInput.value = "";
            cityInput.placeholder = "Not found";
            return;
        }
        const data = await response.json();
        
        fetchAndShowWeather(data.lat, data.lon, `${data.name}, ${data.country}`);
        cityInput.value = "";
        cityInput.placeholder = "Enter city name...";
        sidebar.classList.remove('active'); 
    } catch {
        cityInput.placeholder = "Timeout.";
    }
}

document.getElementById('search-btn').addEventListener('click', searchCity);
document.getElementById('city-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') searchCity();
});
