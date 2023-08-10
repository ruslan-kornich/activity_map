const osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data © <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
});

const cartoLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>'
});

const map = L.map('map', {
    center: [48.459801, 35.009273],
    zoom: 11,
    layers: [osmLayer], // OSM layer will be selected by default
    minZoom: 6,
    maxZoom: 19,
    zoomControl: false // Disable standard proximity/remote buttons
});

L.control.zoom({
     position: 'bottomright'
}).addTo(map);

const baseLayers = {
    "OpenStreetMap": osmLayer,
    "Carto Light": cartoLayer
};

// Add a layer toggle controller. By default, it will be in the upper right corner.
L.control.layers(baseLayers).addTo(map);


let currentMarkers = [];

// Load visible markers and activities
function loadVisibleMarkers() {
    const bounds = map.getBounds();
    const minLat = bounds.getSouth();
    const maxLat = bounds.getNorth();
    const minLng = bounds.getWest();
    const maxLng = bounds.getEast();

    fetchActivities();
    fetchMarkers(minLat, maxLat, minLng, maxLng);
}

function fetchActivities() {
    fetch('/api/activities/')
        .then(response => response.json())
        .then(activities => {
            const activityCheckboxes = document.getElementById('activity-checkboxes');
            activityCheckboxes.innerHTML = '';

            activities.forEach(activity => {
                // Create a container for the toggle switch and its label
                const switchContainer = document.createElement('div');
                switchContainer.classList.add('switch');

                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.id = `activity-${activity.id}`;
                checkbox.value = activity.id;
                checkbox.checked = true;
                checkbox.addEventListener('change', updateMarkers);

                const switchLabel = document.createElement('label');
                switchLabel.htmlFor = `activity-${activity.id}`;
                switchLabel.classList.add('slider', 'round');

                const activityLabel = document.createElement('label');
                activityLabel.htmlFor = `activity-${activity.id}`;
                activityLabel.textContent = activity.name;

                switchContainer.appendChild(checkbox);
                switchContainer.appendChild(switchLabel);
                switchContainer.appendChild(activityLabel); // Add a label inside the container

                activityCheckboxes.appendChild(switchContainer);
            });
        })
        .catch(error => console.error("There was a problem fetching activities:", error));
}




function fetchMarkers(minLat, maxLat, minLng, maxLng) {
    const url = `/api/markers/?minLat=${minLat}&maxLat=${maxLat}&minLng=${minLng}&maxLng=${maxLng}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            // Clear current markers and add new ones
            currentMarkers.forEach(item => item.marker.remove());
            currentMarkers = [];

            data.forEach(markerData => {
                const latLng = [markerData.lat, markerData.lng];
                const icon = L.AwesomeMarkers.icon({
                    icon: markerData.activity.icon.replace('fa-', ''),
                    prefix: 'fa',
                    markerColor: markerData.activity.color
                });
                const marker = L.marker(latLng, { icon: icon }).addTo(map);
                const popupContent = `
                    <h4>${markerData.activity.name}</h4>
                    <p>Quantity: ${markerData.quantity}</p>
                    <p>Date: ${markerData.date}</p>
                    <p>Place: ${markerData.place}</p>
                `;
                marker.bindPopup(popupContent);
                currentMarkers.push({ marker: marker, activityId: markerData.activity.id });
            });

            updateMarkers();
        })
        .catch(error => console.error("There was a problem fetching the markers:", error));
}

function getSelectedActivities() {
    return Array.from(document.querySelectorAll('#activity-checkboxes input:checked')).map(checkbox => checkbox.value);
}

function updateMarkers() {
    const selectedActivities = getSelectedActivities();

    currentMarkers.forEach(item => {
        if (selectedActivities.includes(item.activityId.toString())) {
            if (!map.hasLayer(item.marker)) {
                map.addLayer(item.marker);
            }
            item.marker.on('click', onMarkerClick);
        } else {
            if (map.hasLayer(item.marker)) {
                map.removeLayer(item.marker);
            }
            item.marker.off('click', onMarkerClick);
        }
    });

    localStorage.setItem('selectedActivities', JSON.stringify(selectedActivities));
}

function onMarkerClick(e) {
    e.target.openPopup();
}

function loadMarkersBasedOnFilters() {
    const bounds = map.getBounds();
    const minLat = bounds.getSouth();
    const maxLat = bounds.getNorth();
    const minLng = bounds.getWest();
    const maxLng = bounds.getEast();

    fetchMarkers(minLat, maxLat, minLng, maxLng);
}

map.on('moveend', function() {
    loadMarkersBasedOnFilters();
    updateMarkers(); // update markers based on the current state of filters
});

document.addEventListener('DOMContentLoaded', () => {
    const savedSelectedActivities = localStorage.getItem('selectedActivities');
    const selectedActivities = savedSelectedActivities ? JSON.parse(savedSelectedActivities) : [];

    setTimeout(() => {
        const checkboxes = document.querySelectorAll('#activity-checkboxes input');
        checkboxes.forEach(checkbox => {
            checkbox.checked = selectedActivities.includes(checkbox.value);
        });

        loadVisibleMarkers(); // initial loading of tokens and activities
        updateMarkers(); // apply the saved filters
    }, 0);
});