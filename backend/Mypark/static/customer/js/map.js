

var map = L.map('map');

map.setView([51.505, -0.09], 13);



L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {

    maxZoom: 19,

    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'

}).addTo(map);



navigator.geolocation.watchPosition(success, error);

let marker, circle, zoomed;



function success(pos){

    const lat = pos.coords.latitude;

    const lng = pos.coords.longitude;

    const accuracy = pos.coords.accuracy;



    if(marker){

        map.removeLayer(marker);

        map.removeLayer(circle);

    }



    marker = L.marker([lat, lng]).addTo(map);

    circle = L.circle([lat, lng], { radius: accuracy }).addTo(map);



    if(zoomed){

        zoomed = map.fitBounds(circle.getBounds());

    }



    map.setView([lat, lng]);

}



function error(err){

    if(err === 1){

        alert("Please allow geolocation access");

    } else {

        alert("Cannot get current location");

    }

}



// Code to open the panel and populate it with place details when you search

const infoContent = document.getElementById('infoContent');



function openInfoPanel() {

    infoPanel.classList.add('open');

}



function closeInfoPanel() {

    infoPanel.classList.remove('open');

}



document.getElementById('searchButton').addEventListener('click', function () {

    const query = document.getElementById('searchInput').value;



    // Define the bounding box coordinates for Kathmandu Valley

    const kathmanduValleyBounds = '85.2154,27.5142,85.4685,27.7465';



    // Use the Nominatim geocoding service to search for the location within Kathmandu Valley

    fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${query}&viewbox=${kathmanduValleyBounds}`)

        .then(response => response.json())

        .then(data => {

            if (data && data.length > 0) {

                const result = data[0];

                const lat = parseFloat(result.lat);

                const lon = parseFloat(result.lon);



                // Clear existing marker

                if (marker) {

                    map.removeLayer(marker);

                }



                // Add a new marker for the search result

                marker = L.marker([lat, lon]).addTo(map);

                map.setView([lat, lon], 13);



                // Open the panel

                openInfoPanel();

            } else {

                alert('Location not found within Kathmandu Valley.');

            }

        })

        .catch(error => {

            console.error('Error:', error);

        });

});



document.getElementById('clearButton').addEventListener('click', function () {

    document.getElementById('searchInput').value = ''; // Clear the input

    closeInfoPanel(); // Close the panel

});



// Open the panel by default

openInfoPanel();


