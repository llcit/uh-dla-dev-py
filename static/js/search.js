function main() {
	
	//Eliminate filter in search view
	$( ".glyphicon" ).click(function() {
	 	$(this).closest('.btn').remove();

	});
	//Eliminate filter for dynamic created elements (New filters) It only works this way for dynamic objects
	$('body').on('click', '.glyphicon', function() {
    	$(this).closest('.btn').remove();
	});
	//Add new filters
	$( "#filter" ).click(function() {
		var query = $("#query").val()
		var type = $("#type").val()
		var keyword = $("#keyword").val()
	 	$('<button type="button" class="btn btn-default btn-lg">' + query + ' ' + type +'<b> "' + keyword + '" </b> <span class="glyphicon glyphicon-remove"></span></button>').insertAfter('div.current');

	});
}

//############## End MAIN function ###############################

$(main);
