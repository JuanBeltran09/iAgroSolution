document.addEventListener('DOMContentLoaded', function () {
    var map = L.map('map').setView([4.639386,-74.082412],10 );

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
});
