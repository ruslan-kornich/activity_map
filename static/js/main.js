var map = L.map('map').setView([48.5, 35], 7);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var markers = []; // Хранилище для маркеров
var activityLayers = {}; // Хранилище для слоев активностей
var markerDataByLocationAndActivity = {}; // Хранилище для данных маркеров по местоположению и активности

// Загрузка данных маркеров через API
fetch('/api/markers/')
    .then(response => response.json())
    .then(data => {
        var uniqueActivities = new Set(data.map(marker => marker.activity.name));

        var activityCheckboxes = document.getElementById('activity-checkboxes');
        uniqueActivities.forEach(activity => {
            var checkboxContainer = document.createElement('label');
            checkboxContainer.innerHTML = `<input type="checkbox" value="${activity}" checked> ${activity}<br>`;
            activityCheckboxes.appendChild(checkboxContainer);
        });

        var checkboxes = document.querySelectorAll('#activity-checkboxes input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function () {
                var selectedActivities = Array.from(checkboxes)
                    .filter(checkbox => checkbox.checked)
                    .map(checkbox => checkbox.value);

                updateMarkerVisibility(selectedActivities);
            });
        });

        data.forEach(marker => {
            var lat = marker.location[0];
            var lon = marker.location[1];
            var activity = marker.activity.name;
            var quantity = marker.quantity;
            var date = marker.date;
            var place = marker.place;
            var iconClass = marker.activity.icon; // Иконка для активности из базы данных
            var color = marker.activity.color; // Цвет для активности из базы данных

            // Создаем иконку с использованием AwesomeMarkers
            var icon = L.AwesomeMarkers.icon({
                icon: iconClass, // Иконка для активности из базы данных
                prefix: 'fa', // Префикс класса иконок Font Awesome
                markerColor: color // Цвет маркера для активности из базы данных
            });

            // Добавляем маркер на слой активности, вместо добавления его прямо на карту
            if (!activityLayers[activity]) {
                activityLayers[activity] = L.layerGroup().addTo(map);
            }

            var markerPopup = L.popup().setContent(`<b>${place}</b><br>Activity: ${activity}<br>Quantity: ${quantity}<br>Date: ${date}`);
            var markerInstance = L.marker([lat, lon], { icon: icon }).addTo(activityLayers[activity]).bindPopup(markerPopup);
            markerInstance.on('click', function () {
                // Отображаем информацию о маркерах в боковом меню
                var markerInfoList = document.getElementById('marker-list');
                markerInfoList.innerHTML = ''; // Очищаем список

                // Получаем все записи с данным ключом и добавляем их в список
                var key = lat.toString() + lon.toString() + activity;
                var markerDataList = markerDataByLocationAndActivity[key];
                markerDataList.forEach(markerData => {
                    var listItem = document.createElement('li');
                    listItem.innerHTML = `<b>${markerData.place}</b><br>Activity: ${markerData.activity}<br>Quantity: ${markerData.quantity}<br>Date: ${markerData.date}`;
                    markerInfoList.appendChild(listItem);
                });
            });

            markers.push({ marker: markerInstance, activity, isVisible: true });

            // Формируем уникальный ключ на основе местоположения и активности
            var key = lat.toString() + lon.toString() + activity;

            // Если такой ключ уже существует, добавляем информацию в объект
            if (key in markerDataByLocationAndActivity) {
                markerDataByLocationAndActivity[key].push({
                    activity: activity,
                    quantity: quantity,
                    date: date,
                    place: place
                });
            } else {
                // Если ключа еще нет, создаем новую запись в объекте
                markerDataByLocationAndActivity[key] = [{
                    activity: activity,
                    quantity: quantity,
                    date: date,
                    place: place
                }];
            }
        });

        updateMarkerVisibility = function (selectedActivities) {
            // Удаляем все слои активности
            for (var activity in activityLayers) {
                map.removeLayer(activityLayers[activity]);
            }

            // Добавляем выбранные слои активности обратно
            selectedActivities.forEach(activity => {
                if (activity in activityLayers) {
                    map.addLayer(activityLayers[activity]);
                }
            });
        };
    })
    .catch(error => console.error('Error fetching markers:', error));
