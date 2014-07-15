//agon 2014 June Java Script to launch map visualizations for elements in Scholarspace 


//############ Variables Declaration #####################
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
	}
}

//############## End MAIN function ###############################

$(main);
