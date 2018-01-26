$(function() {
	// Init Google Maps
	var maps = $('.map-placeholder');
	if (maps.length > 0) {
		$.each(maps, function() {
			initMap($(this));
		});
	}
});

function initMap(element) 
{
  	var mapElement = $(element).find('.map-init').get(0);
	var map = new google.maps.Map(mapElement);

	var boundsObject = {
		north: parseFloat($(element).find('input.north').val()),
		south: parseFloat($(element).find('input.south').val()),
		east: parseFloat($(element).find('input.east').val()),
		west: parseFloat($(element).find('input.west').val())
	};

	var bounds = new google.maps.LatLngBounds(
    	new google.maps.LatLng(boundsObject.south, boundsObject.east),
    	new google.maps.LatLng(boundsObject.north, boundsObject.west)
	);

	// Define the rectangle and set its editable property to true.
	var rectangle = new google.maps.Rectangle({
		bounds: bounds
	});

	rectangle.setMap(map);
	map.fitBounds(bounds);

	return true;
}