//Function to create table
function drawTable(map) {
  	var data = new google.visualization.DataTable();
  	data.addColumn('string', 'Record');
  	// data.addColumn('string', 'Creator');
  	data.addColumn('string', 'Date');
    data.addColumn('string', 'Contributor');
    data.addColumn('string', 'Language');
    // data.addColumn('string', 'Description');
    data.addColumn('string', 'North');
    data.addColumn('string', 'East');
	  data.addRows(json.length);
  	for (var i=0; i<json.length; i++){
	  data.setCell(i, 0, json[i].Record);
	  // data.setCell(i, 0, json[i].Creator);
	  data.setCell(i, 1, json[i].Date);
    data.setCell(i, 2, json[i].Contributor);
    data.setCell(i, 3, json[i].Language);
    // data.setCell(i, 5, json[i].Description);
    data.setCell(i, 4, json[i].North);
    data.setCell(i, 5, json[i].East);
	}

	var table_options = {
		showRowNumber: true,
		height: '350px',
		width: '600px',
		page: 'enable',
		pageSize: 20
	}

  	var table = new google.visualization.Table(document.getElementById('table'));
  	table.draw(data, table_options);

  	google.visualization.events.addListener(table, 'select', function() {
    	var row = table.getSelection()[0].row;
    	for(i in extra_dataNoDuplates) {
    		if(extra_dataNoDuplates[i]==data.getValue(row, 3)) {
    			if (selected_infowindow.length!=0) selected_infowindow.pop().close(map);
    			infowindow[i].open(map);
    			selected_infowindow.push(infowindow[i]);
    		}
    	}
  	});
}