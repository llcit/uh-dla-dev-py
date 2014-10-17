function initializeLanguageMap() {
  	//Save languages center coordinates to plot into the map
	for (var i = 0; i<json.length; ++i) {
		circleCenter[i] = new google.maps.LatLng(json[i].east, json[i].north)
	}

	if (typeof circleCenter[0] != 'undefined') 
		var mapcenter = new google.maps.LatLng(circleCenter[0].k, circleCenter[0].B);
	else 
		var mapcenter = new google.maps.LatLng(0, 0);

	
	var mapOptions = {
		zoom: 1,
		minZoom:1,
		center: mapcenter,
		mapTypeId: google.maps.MapTypeId.SATELLITE
	};

	var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);


	for (var i = 0; i<circleCenter.length; i++) {

		// var languageOptions = {
		//   strokeColor: '#fff',
		//   strokeOpacity: 0.0,
		//   strokeWeight: 1,
		//   fillColor: '#fff',
		//   fillOpacity: 0.1,
		//   map: map,
		//   center: circleCenter[i],
		//   radius: 1000
		// };

		// // Add the circle for this language to the map.
		// languageCircle [i] = new google.maps.Circle(languageOptions);

		// //Text to display when hovering languages on map
		// text = "";
		// contentString.push('<p> <b>Language:</b> ' + languageCenter[i] + '<br> <b>Coordinates:</b> ' + circleCenter[i] + '</p>')

		// Add the marker for this language to the map.
		var marker = new google.maps.Marker({
		      position: circleCenter[i],
		      map: map,
		      // title: 'Languages: ' + languageCenter[i]
		});

		google.maps.event.addListener(marker, 'click', function() {
			map.setZoom(12);
			map.setCenter(this.getPosition());
			console.log(this);
		});
	}



	// for (x in languageCircle) {
	// 	google.maps.event.addListener(languageCircle[x], 'click', makeMapListener(infowindow[x], map));
	// }

	// function makeMapListener(window, map) {
 //  		return function() { window.open(map) };
	// }

	
	return map;
}

