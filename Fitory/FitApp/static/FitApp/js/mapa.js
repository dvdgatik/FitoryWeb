$(function(){
	if(navigator.geolocation){
		navigator.geolocation.getCurrentPosition(getCoords, getError);
	}else{
		initialize(25.478124, -100.944095);
	}

	function getCoords(position){
		var lat = latF;
		var lng = lngF;
		initialize(lat, lng);
	}

	function getError(err){
		initialize(25.478124, -100.944095);
	}

	function initialize(lat,lng){
		var latlng = new google.maps.LatLng(lat, lng);
		var mapSettings = {
			center: latlng,
			zoom: 15,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		}
		map = new google.maps.Map($('#mapa').get(0),mapSettings);

		var marker = new google.maps.Marker({
			position: latlng,
			map: map,
			draggable: true,
			title: 'Seleccione una ubicación'
		});

		google.maps.event.addListener(marker, 'position_changed', function(){
			getMarkerCoords(marker);
		}); 
	}

	function getMarkerCoords(marker){
		var markerCoords = marker.getPosition();
		$('#lat').val( markerCoords.lat() );
		$('#lng').val( markerCoords.lng() );
	}
});