var map = L.map('map').setView([48.5, 35], 7);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Загрузка данных маркеров через API
    fetch('/api/markers/')
        .then(response => response.json())
        .then(data => {
            // Создаем объект для хранения информации о маркерах с одинаковым местоположением и активностью
            var markerDataByLocationAndActivity = {};

            // Получаем все уникальные активности для фильтрации
            var uniqueActivities = new Set(data.map(marker => marker.activity.name));

            // Добавляем чекбоксы для выбора активностей в фильтре
            var activityCheckboxes = document.getElementById('activity-checkboxes');
            uniqueActivities.forEach(activity => {
                var checkboxContainer = document.createElement('label');
                checkboxContainer.innerHTML = `<input type="checkbox" value="${activity}" checked> ${activity}<br>`;
                activityCheckboxes.appendChild(checkboxContainer);
            });

            // Обработчик события изменения выбранных активностей в фильтре
            var checkboxes = document.querySelectorAll('#activity-checkboxes input[type="checkbox"]');
            checkboxes.forEach(checkbox => {
                checkbox.addEventListener('change', function() {
                    var selectedActivities = Array.from(checkboxes)
                        .filter(checkbox => checkbox.checked)
                        .map(checkbox => checkbox.value);

                    // Перебираем все точки на карте и устанавливаем видимость в зависимости от выбранных активностей
                    data.forEach(marker => {
                        var lat = marker.location[0];
                        var lon = marker.location[1];
                        var activity = marker.activity.name;
                        var isVisible = selectedActivities.includes(activity);
                        var key = lat.toString() + lon.toString() + activity;

                        map.eachLayer(layer => {
                            if (layer instanceof L.Marker && layer.options.icon.options.markerColor === marker.activity.color) {
                                if (isVisible) {
                                    layer.setOpacity(1);
                                } else {
                                    layer.setOpacity(0);
                                }
                            }
                        });
                    });
                });
            });

            // Обрабатываем каждую запись из полученных данных и добавляем маркеры на карту
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

                // Добавляем маркер на карту и обработчик клика
                var markerPopup = L.popup().setContent(`<b>${place}</b><br>Activity: ${activity}<br>Quantity: ${quantity}<br>Date: ${date}`);
                L.marker([lat, lon], { icon: icon }).addTo(map).bindPopup(markerPopup).on('click', function() {
                    // Отображаем информацию о маркерах в боковом меню
                    var markerInfoList = document.getElementById('marker-list');
                    markerInfoList.innerHTML = ''; // Очищаем список

                    // Получаем все записи с данным ключом и добавляем их в список
                    var markerDataList = markerDataByLocationAndActivity[key];
                    markerDataList.forEach(markerData => {
                        var listItem = document.createElement('li');
                        listItem.innerHTML = `<b>${markerData.place}</b><br>Activity: ${markerData.activity}<br>Quantity: ${markerData.quantity}<br>Date: ${markerData.date}`;
                        markerInfoList.appendChild(listItem);
                    });
                });

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
        });