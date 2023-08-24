const cartoLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>'
});

const map = L.map('map', {
    center: [48.459801, 35.009273],
    zoom: 11,
    layers: [cartoLayer], // Only the CARTO layer
    minZoom: 9,
    maxZoom: 13,
    zoomControl: false // Disable standard proximity/remote buttons
});

L.control.zoom({
     position: 'bottomright'
}).addTo(map);

fetch('https://deepstatemap.live/api/history/1687169321/geojson')
  .then(function (response) {
    if (response.ok) {
      return response.json();
    } else {
      throw new Error('Ошибка загрузки полигонов');
    }
  })
  .then(function (data) {
    // Filter the data to display only polygons
    const polygons = data.features.filter(feature => feature.geometry.type !== 'Point');

    // Create a new GeoJSON object with polygons only
    const geoJsonData = {
      type: 'FeatureCollection',
      features: polygons
    };

    L.geoJSON(geoJsonData, {
      style: function (feature) {
        return {
          color: feature.properties.stroke,
          fillColor: feature.properties.fill,
          weight: feature.properties['stroke-width'],
          fillOpacity: feature.properties['fill-opacity']
        };
      }

    }).addTo(map);
  })
  .catch(function (error) {
    console.error(error);
  });


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
            // Clear current markers
            currentMarkers.forEach(item => item.marker.remove());
            currentMarkers = [];

            // Process each marker data without adding to map yet
            data.forEach(markerData => {
                const latLng = [markerData.lat, markerData.lng];
                const icon = L.AwesomeMarkers.icon({
                    icon: markerData.activity.icon.replace('fa-', ''),
                    prefix: 'fa',
                    markerColor: markerData.activity.color
                });
                const marker = L.marker(latLng, { icon: icon });
                marker.activityName = markerData.activity.name; // Add activity name
                marker.placeName = markerData.place; // Add the name of the place
                const popupContent = `
                    <h3>Activity: ${markerData.activity.name}</h3>
                    <p>Place: ${markerData.place}</p>
                `;
                marker.bindPopup(popupContent);
                currentMarkers.push({ marker: marker, activityId: markerData.activity.id });
            });

            // Now, add all markers to the map
            currentMarkers.forEach(item => item.marker.addTo(map));
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

    const activityName = e.target.activityName;
    const placeName = e.target.placeName;

    // Reset the previous content of the list
    $('#marker-list').empty();

    // Add new content
    $('#marker-list').append(`<li>Activity: ${activityName}</li>`);
    $('#marker-list').append(`<li>Place: ${placeName}</li>`);

    fetchActivitiesForPlace(placeName, activityName);
}

function fetchActivitiesForPlace(placeName, activityName) {
    const url = `/api/activities_for_place/${placeName}/${activityName}/`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            // Reset the previous content of the list
            $('#marker-list').empty();

            // Create a new container for messages
            const messagesContainer = $('<div></div>');

            // Iterate over all items received from API
            data.forEach(item => {
            const message = `
                            <div class="marker-message">
                            <div><strong>Place:</strong> ${item.place}</div>
                            <div><strong>Activity:</strong> ${item.activity.name}</div>
                            <div><strong>Quantity:</strong> ${item.quantity}</div>
                            <div><strong>Beneficiary:</strong> ${item.beneficiary}</div>
                            <div><strong>Date:</strong> ${item.date}</div>
                         </div>
                            `;
    messagesContainer.append(message);
});
            // Append the messages container to the list
            $('#marker-list').append(messagesContainer);
        })
        .catch(error => console.error("There was a problem fetching activities for place:", error));
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