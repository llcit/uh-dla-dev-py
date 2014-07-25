//agon 2014 June Java Script to manage the search menu for elements in the Kaipuleohone Collection
//This is the Js corresponding with the search page and collection page results box

//DOM Variables
records = $(".searchBox").children();

//variables
var pivot = 10;
var num_results = 10;
var actualPage = 1;

function main() {



	//Initially we show 10 elements of each group
	records.slice(pivot,records.length).hide();
	
	boxPaginator(records,pivot,actualPage,num_results);
	if (pivot < records.length){
		records.slice(pivot,records.length).hide();
	}
}

//############## End MAIN function ###############################

$(main);

//##############Paginator function ################################
function boxPaginator (records,pivot,actual_page,num_results) {

	var pages = Math.ceil(records.length/pivot);

	//Click Handlers
	$(".previous").click(function(){
		if(actual_page!=1){
			actual_page--;
			$(".next").removeClass("disabled");
			showItems(actual_page,pages,".previous",records,"prev",num_results);
		}
	});
	$(".next").click(function(){
		if(actual_page!=pages){
			actual_page++;
			$(".previous").removeClass("disabled");
			showItems(actual_page,pages,".next",records,"next",num_results);
		}
	});

	//Search Box menu UI elements
	//Pivots
	$("#pivot10").click(function(){
		pivot = 10;
		num_results = 10;
		records.slice(0,pivot).show();
		records.slice(pivot,records.length).hide();
		pages = Math.ceil(records.length/pivot);
		actual_page =1;
		if (pages > actual_page) {
			$(".next").removeClass("disabled");
		}
		$(".previous").addClass("disabled");
		boxPaginator(records,pivot,actualPage,num_results);
	});
	$("#pivot20").click(function(){
		pivot = 20;
		num_results = 20;
		records.slice(0,pivot.length).show();
		records.slice(pivot,records.length).hide();
		pages = Math.ceil(records.length/pivot);
		actual_page =1;
		if (pages > actual_page) {
			$(".next").removeClass("disabled");
		}
		$(".previous").addClass("disabled");
		boxPaginator(records,pivot,actualPage,num_results);
	
	});
	$("#pivot30").click(function(){
		pivot = 30;
		num_results = 30;
		records.slice(0,pivot).show();
		records.slice(pivot,records.length).hide();
		pages = Math.ceil(records.length/pivot);
		actual_page =1;
		if (pages > actual_page) {
			$(".next").removeClass("disabled");
		}
		$(".previous").addClass("disabled");
		boxPaginator(records,pivot,actualPage,num_results);
		
	});
	$("#pivot50").click(function(){
		pivot = 50;
		num_results = 50;
		records.slice(0,pivot).show();
		records.slice(pivot,records.length).hide();
		pages = Math.ceil(records.length/pivot);
		actual_page =1;
		if (pages > actual_page) {
			$(".next").removeClass("disabled");
		}
		$(".previous").addClass("disabled");
		boxPaginator(records,pivot,actualPage,num_results);

	});
	$("#pivotAll").click(function(){
		records.show();
		pivot = records.length;
		pages = 1;
		actual_page =1;
		$(".next").addClass("disabled");
		$(".previous").addClass("disabled");
	});

	function showItems (actual_page,num_pages,elements,collection,type,num_results){
		var pivot=actual_page*num_results;
		//last page
		if(actual_page==num_pages){
			$(elements).addClass("disabled");
			collection.slice(pivot-num_results,collection.length).show();
			collection.slice(0,pivot-num_results).hide();
		}
		//middle pages
		if(actual_page<num_pages && actual_page!=1){
			if(type=="next"){
				collection.slice(pivot-num_results,pivot).show();
				collection.slice(0,pivot-num_results).hide();
				collection.slice(pivot,collection.length).hide();
			}else{ //type previous
				collection.slice(pivot-num_results,pivot).show();
				collection.slice(0,pivot-num_results).hide();
				collection.slice(pivot,collection.length).hide();
			}
			

		}
		//first page
		if(actual_page==1){
			$(elements).addClass("disabled")
			collection.slice(0,pivot).show()
			collection.slice(pivot ,collection.length).hide()	
		}
	}
}
