// harvester.js
jQuery(function($) {
	// $("div.radio").click(function () {
	// 	$(this).parent().removeClass("required");
	// });

	$("#collection_form").submit(function () {
		var repo = $("#repo").val();
		var postdata = $(".collection").serializeArray();
		console.log("POSTDATA:" + postdata);
		$.post("/harvest/repository/"+repo, postdata, function(data) {
			for(i in data) {
				console.log(i);
			}
		});	
	});


	$(document).ready(function() {});
});
