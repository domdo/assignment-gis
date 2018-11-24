var mapOptions = {
    zoom: 10,
    center: [35.685360,  139.753372],
}

var map = new L.map('map', mapOptions);
map.attributionControl.addAttribution('<a href="https://www.mapbox.com/">Mapbox</a>');
map.attributionControl.addAttribution('<a href="https://www.openstreetmap.org/#map=2/34.2/71.5">OpenStreetMap</a>');

var acces_token = 'pk.eyJ1IjoiZG9tZG8iLCJhIjoiY2ptcTJmOGF3MTRlZTNwbHU1d3p0d3c1aCJ9.OAGkPmpZYDnmLaN4cQtsEw';
var mapboxlayer = new L.tileLayer('https://api.mapbox.com/styles/v1/domdo/cjnt3gv5q3hxq2sqg0fx3zmp3/tiles/256/{z}/{x}/{y}?access_token='+acces_token);

map.addLayer(mapboxlayer);


function getMapPosition(element, lat, lon) {
    map.on('click', function (e) {
        if ((element.id.localeCompare('nearPosButton') == 0) || (element.id.localeCompare('stationRoutes') == 0)){
            if (typeof myPosMarker !== 'undefined') {
                map.removeLayer(myPosMarker);
            }
            myPosMarker = L.marker([e.latlng.lat, e.latlng.lng], {icon: myPosIcon});
            myPosMarker.bindPopup('Moja pozícia').openPopup();
            myPosMarker.addTo(map);
        }
        document.getElementById(lat).value = e.latlng.lat;
        document.getElementById(lon).value = e.latlng.lng;
    });
    element.text = "Potvrď pozíciu";
    element.removeEventListener("click", getMapPosition);
    element.addEventListener('click', function(){
        stopMapPositioning(element, lat, lon);
    });
}

function stopMapPositioning(element, lat, lon) {
    map.off('click');
    element.text = "Nastav pozíciu";
    element.removeEventListener("click", stopMapPositioning);
    element.addEventListener('click', function(){
        getMapPosition(element, lat, lon);
    });
}

function getData(url) {
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            if (this.status == 200) {
                if (typeof markerLayer !== 'undefined'){
                    map.removeLayer(markerLayer);
                }
                var response = JSON.parse(this.responseText);
                markerLayer = L.geoJson(response, {style: myStyle, onEachFeature: onEachFeature}).addTo(map);
                console.log(response);
            }
            else {
                alert("Something went wrong!");
            }
        }
    }
    xhttp.open("GET", url, true);
    xhttp.send();
    return;
}

function clearMap() {
    map.eachLayer(function (l) {
        if (mapboxlayer != l) {
            map.removeLayer(l);
        }
    });
}

var myStyle = {
    "color": "#880034"
};

function onEachFeature(feature, layer) {
    if (feature.properties && feature.properties.popupContent) {
        layer.bindPopup(feature.properties.popupContent);
    }
}

var myPosIcon = L.icon({
    iconUrl: 'icons/myposition.png',
    iconSize:     [26, 40],
    iconAnchor:   [12, 39],
    popupAnchor:  [0, -40]
});

var acc = document.getElementsByClassName("accordion");
var i;
for (i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function() {
        /* Toggle between adding and removing the "active" class,
        to highlight the button that controls the panel */
        this.classList.toggle("active");

        /* Toggle between hiding and showing the active panel */
        var panel = this.nextElementSibling;
        if (panel.style.display === "block") {
            panel.style.display = "none";
        } else {
            panel.style.display = "block";
        }
    });
}