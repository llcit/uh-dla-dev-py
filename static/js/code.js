//agon 2014 June Java Script to launch map visualizations for elements in Scholarspace 


//############  GlOBAL Variables Declaration #####################
var map;
var TILE_SIZE = 256;
var languageMap = [];

//coordinates variables
var north = [];
var east = [];
//Arrays to save coordinates with or withoput duplicates
var languageCenter = [];
var extra_data = [];
var extra_dataNoDuplates = [];
var languagesCenterNoDuplicates = [];
//Variables to paint the languages as circles in the map (center and the actual circles)
var circleCenter = []; 
var languageCircle = [];
var contentString = [];
var infowindow = [];
var selected_infowindow = [];

//DOM Variables
	var collection_items = $(" #collection .list-group").children();
	var collection_pages = Math.ceil(collection_items.length/10);
	var language_items = $(" #language .list-group").children();
	var language_pages = Math.ceil(language_items.length/10);
	var depositor_items = $(" #depositor .list-group").children();
	var depositor_pages = Math.ceil(depositor_items.length/10);
	//We store the page it is being showned for each group Collection, Language, Depositor initially 1. First Page
	var collection_pager=1;
	var depositor_pager=1;
	var language_pager=1;
	var first_cut=10;

//############# End of Variables declaration #################  

//############# MAIN Function ################################

//load googlecharts for the table
google.load('visualization', '1', {'packages': ['map','table']});

function main() {
	google.setOnLoadCallback(googleReady);
	//Function to launch googleAPI
	function googleReady() {
		//Paint map if there are elements with coverage
		if (json.length>0){
			map = initializeLanguageMap();
			drawTable(map);
		//Else print No Geodata Message
		}else{
			$("#map-canvas" ).toggle();
			$("#table").toggle();
			$("#nogeotext").toggle();

		}
	paginator();
	}
}

//############## End MAIN function ###############################

$(main);

//##############Paginator function ################################
function paginator () {


	//Initially we show 10 elements of each group
	collection_items.slice(first_cut,collection_items.length).hide()
	language_items.slice(first_cut,language_items.length).hide()
	depositor_items.slice(first_cut,depositor_items.length).hide()

	//Click Handlers
	$(".previous .collection").click(function(){
		if(collection_pager!=1){
			collection_pager--;
			$("#next_col").removeClass("disabled")
			showItems(collection_pager,collection_pages,"#prev_col",collection_items,"prev")
		}
	});
	$(".next .collection").click(function(){
		if(collection_pager!=collection_pages){
			collection_pager++;
			$("#prev_col").removeClass("disabled")
			showItems(collection_pager,collection_pages,"#next_col",collection_items,"next")
		}
	});
	$(".previous .language").click(function(){
		if(language_pager!=1){
			language_pager--;
			$("#next_lan").removeClass("disabled")
			showItems(language_pager,language_pages,"#prev_lan",language_items,"prev")
		}
	});
	$(".next .language").click(function(){
		if(language_pager!=language_pages){
			language_pager++;
			$("#prev_lan").removeClass("disabled")
			showItems(language_pager,language_pages,"#next_lan",language_items,"next")
		}
	});
	$(".previous .depositor").click(function(){
		if(depositor_pager!=1){
			depositor_pager--;
			$("#next_dep").removeClass("disabled")
			showItems(depositor_pager,depositor_pages,"#prev_dep",depositor_items,"prev")
		}
	});
	$(".next .depositor").click(function(){
		if(depositor_pager!=depositor_pages){
			depositor_pager++;
			$("#prev_dep").removeClass("disabled")
			showItems(depositor_pager,depositor_pages,"#next_dep",depositor_items,"next")
		}
	});

	function showItems (actual_page,num_pages,elements,collection,type){
		var pivot=actual_page*10;;
		//last page
		if(actual_page==num_pages){
			$(elements).addClass("disabled")
			collection.slice(pivot-10,collection.length).show()
			collection.slice(0,pivot-10).hide()	
		}
		//middle pages
		if(actual_page<num_pages && actual_page!=1){
			if(type=="next"){
				collection.slice(pivot-10,pivot).show()
				collection.slice(0,pivot-10).hide()
				collection.slice(pivot,collection.length).hide()
			}else{ //type previous
				collection.slice(pivot-10,pivot).show()
				collection.slice(0,pivot-10).hide()
				collection.slice(pivot,collection.length).hide()
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