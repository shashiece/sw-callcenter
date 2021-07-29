var totalItem = 1;
var selectNode;
var GOTOData = [];
$('document').ready(function () {
	new Treant(chart_config);
	$('.node.nodeExample').click(function () {
		selectNode = this;
		reset();
		$('#nodeSelect').hide();
		$('#ivrFlowModal').modal('show');
		if ($(this).attr("id") == "1") {
			$('button#editBtn').prop('disabled', true);
			$('button#deleteBtn').prop('disabled', true);
		}
		$('.inputBtnHolder').show();
	})
	var IvrFlowId = window.location.pathname.split("/")[2]; // Returns path only (/path/example.html)


	$.ajax('/jquery/getjsondata', 
	{
		dataType: 'json', // type of response data
		timeout: 500,     // timeout milliseconds
		success: function (data,status,xhr) {   // success callback function
			$('p').append(data.firstName + ' ' + data.middleName + ' ' + data.lastName);
		},
		error: function (jqXhr, textStatus, errorMessage) { // error callback 
			$('p').append('Error: ' + errorMessage);
		}
	});

})

if (GOTOData.length > 0) {
	updateGOTOData();
	drawLine();
}

function addNodeModal() {
	if (selectNode !== undefined) {
		$('.addWindow').show();
		$('.inputBtnHolder').hide();
		$('#nodeSelect').show();
		$('#edit-btn').hide();
		$('#save-btn').show();
		$('#delelte-btn').hide();
		$("#addAgentModalLabel").text("Enter Node details to Add");
	}
}


function deleteNodeModal() {
	if (selectNode !== undefined) {
		$('#edit-btn').hide();
		$('#save-btn').hide();
		$('#delete-btn').show();
		$('.inputBtnHolder').hide();
		$('.deleteWindow').show();
		$('#nodeSelect').hide();
		$("#addAgentModalLabel").text("Delete Node");
	}
}

function editNodeModal() {
	if (selectNode !== undefined) {
		$('.inputBtnHolder').hide();
		$('.addWindow').show();
		$('#save-btn').hide();
		$('#edit-btn').show();
		$('#delelte-btn').hide();
		$("#addAgentModalLabel").text("Enter Node details to Edit");
		createEditConainerforNode();
		$('#nodeSelect').hide();
		$("#select-menu").hide();
	}
}


function createEditConainerforNode() {
	for (var i = 1; i < IVRData.length; i++) {
		if (IVRData[i].id == +$(selectNode).attr("id")) {
			$('#select-container-' + IVRData[i].name.toLowerCase()).show();
			switch (IVRData[i].name) {
				case "Say":
					$('#say-name').val(IVRData[i].nodeName);
					$("textarea[name=say-content-text]").val(IVRData[i].value);
					break;
				case "Hangup":
					$('#hangup-name').val(IVRData[i].nodeName);
				case "Gather":
					$('#gather-name').val(IVRData[i].nodeName);
				case "Queue":
					$('#queue-name').val(IVRData[i].nodeName);
					$("#queue-content").val(IVRData[i].value);
				case "Dial":
					$('#dial-name').val(IVRData[i].nodeName);
					$("#dial-content").val(IVRData[i].value);
			}
		}
	}
}


function onSelectGotoNode() {
	$('#ivrFlowModal').modal('hide');
	var fromNode = $(selectNode).attr("id");
	var toNode = $("#select-goto").val();
	createGOTOData(fromNode, toNode);
	drawLine();

}

function createGOTOData(fromNode, toNode) {
	if (GOTOData.indexOf(fromNode + "-" + toNode) == -1) {
		GOTOData.push(fromNode + "-" + toNode);
	}
}


function createInputAddContainer() {
	if ($('#nodeSelect').val() != null && $('#nodeSelect').val() != undefined) {

		//$('#save-btn').show();
		if ($('#nodeSelect').val() == "Goto") {
			var innerHTML = '<select class="form-select" id="select-goto"  onchange="onSelectGotoNode()">'
			innerHTML += '<option value="" selected disabled>Select node to GO</option>';
			for (var i = 0; i < IVRData.length; i++) {
				innerHTML += '<option value="' + IVRData[i].id + '">' + IVRData[i].name + ' - ' + IVRData[i].nodeName + '</option>';
			}
			innerHTML += '</select>';
			$('#goto-nodes-div-container').empty().append(innerHTML).show();
		} else {
			$('#goto-nodes-div-container').empty().hide();
		}
		$('#nodeSelect').hide();
		$('#select-container-' + $('#nodeSelect').val().toLowerCase()).show();

		$('#addAgentModalLabel').text("Selected item : " + $('#nodeSelect').val());
	}

}

//called while saving the node
function saveNode(param) {
	switch (param) {
		case 'add':
			addNode();
			createTreeMapData();
			break;
		case 'delete':
			deleteNode();
			createTreeMapData();
			reset();
			break;
		case 'edit':
			editNode();
			createTreeMapData();
			break;

	}

	$('#ivrFlowModal').modal('hide');

	$('#basic-example').empty();
	new Treant(chart_config);

	$('.node.nodeExample').click(function () {

		console.log($(this).text());
		reset();
		$('#nodeSelect').hide();
		$('.node.nodeExample').removeClass('selected');
		selectNode = this;

		$(this).addClass('selected');
		$('#ivrFlowModal').modal('show');

		if ($(this).attr("id") == "1") {
			$('button#editBtn').prop('disabled', true);
			$('button#deleteBtn').prop('disabled', true);
		}
		if ($(this).text().startsWith("Hangup")) {
			$('button#addBtn').prop('disabled', true);
		}
		if ($(this).text().startsWith("Gather")) {
			$('button#editBtn').prop('disabled', true);
		}
		
		IVRData.forEach(data => {
			if (data.parent == selectNode.id) {	
				$('button#addBtn').prop('disabled', true);
			}
		});
		
		$('.inputBtnHolder').show();

	});

	updateGOTOData();

	drawLine();
}

function updateGOTOData() {

	for (var i = 0; i < GOTOData.length; i++) {
		var firstMatch = false;
		var secondMatch = false;
		var firstElem = GOTOData[i].split("-")[0];
		var secondElem = GOTOData[i].split("-")[1];
		for (var j = 0; j < IVRData.length; j++) {

			if (IVRData[j].id == firstElem)
				firstMatch = true;
			if (IVRData[j].id == secondElem)
				secondMatch = true;
		}
		if (!(firstMatch && secondMatch)) {
			GOTOData.splice(i, 1);
			i--;
		}
	}
}



function editNode() {
	for (var i = 1; i < IVRData.length; i++) {
		if (IVRData[i].id == +$(selectNode).attr("id")) {
			switch (IVRData[i].name) {
				case "Say":
					IVRData[i].value = $("textarea[name=say-content-text]").val();
					IVRData[i].nodeName = $("#say-name").val();
					break;
				case "Hangup":
					IVRData[i].nodeName = $("#hangup-name").val();
				case "Queue":
					IVRData[i].nodeName = $("#queue-name").val();
					IVRData[i].value = $("#queue-content").val();
				case "Dial":
					IVRData[i].nodeName = $("#dial-name").val();
					IVRData[i].value = $("#dial-content").val();	
			}
			break;
		}
	}
}

function addNode() {
	switch ($('#nodeSelect').val()) {

		case 'Say':
			var id = ++totalItem;
			IVRData.push({
				"id": id,
				"name": "Say",
				"nodeName": $("input[id=say-name]").val(),
				"parent": +$(selectNode).attr("id"),
				"value": $("textarea[name=say-content-text]").val()
			});
			break;
		case 'Queue':
			var id = ++totalItem;
			IVRData.push({
				"id": id,
				"name": "Queue",
				"nodeName": $("#queue-name").val(),
				"parent": +$(selectNode).attr("id"),
				"value": $("#queue-content").val()
			});
			break;
		case 'Dial':
			var id = ++totalItem;
			IVRData.push({
				"id": id,
				"name": "Dial",
				"nodeName": $("#dial-name").val(),
				"parent": +$(selectNode).attr("id"),
				"value": $("#dial-content").val()
			});
			break;
		case 'Hangup':
			var id = ++totalItem;

			IVRData.push({
				"id": id,
				"name": "Hangup",
				"nodeName": $("input[id=hangup-name]").val(),
				"parent": +$(selectNode).attr("id")
			});
			break;
		case 'Gather':
			var id = ++totalItem;
			var validKeys = "";

			$('input#digit[type=number]').each(function (index, elem) {
				if (validKeys.length != 0)
					validKeys += ",";
				validKeys += $(elem).val();
			});

			IVRData.push({
				"id": id,
				"name": "Gather",
				"nodeName": $("input[id=gather-name]").val(),
				"parent": +$(selectNode).attr("id"),
				"validKeys": validKeys,
				"say-text-value": $("textarea[name=gather-say-content-text]").val(),
				"voiceClip": "clip"//$("#select-menu-url-valid").val().split("\\").pop(),
			});
			if (+$('#select-gather-nodes').val() > 0) {
				$('.selected-gather-digits').each(function (index, elem) {
					var childId = ++totalItem
					IVRData.push({
						"id": childId,
						"name": "Digit",
						"nodeName": $(elem).find('.input-digits-value').find('input#digit-name[type=text]').val(),
						"digit": +$(elem).find('.input-digits-value').find('input#digit[type=number]').val(),
						"parent": id
					});

				});
				var childId = ++totalItem;
				IVRData.push({
					"id": childId,
					"name": "Digit",
					"nodeName": "Invalid Digit",
					"digit": "invalid",
					"parent": id
				});
			}
			break;
	}
}


var foundNode = false;
function createTreeMapData() {
	chart_config.nodeStructure = JSON.parse(JSON.stringify(nodeStructure));
	for (var i = 1; i < IVRData.length; i++) {
		iterate(chart_config.nodeStructure, IVRData[i]);
		foundNode = false;
	}
}

function iterate(obj, childObj) {
	for (var property in obj) {
		if (obj.hasOwnProperty(property)) {

			if (property == "HTMLid" && obj[property] == childObj.parent) {
				foundNode = true;
			}

			if (typeof obj[property] == "object") {
				if (!foundNode) {
					iterate(obj[property], childObj);
				} else {
					if (property == "children") {
						createNode(obj[property], childObj);
						foundNode = false;
					}
				}
			}
		}
	}

}

//create the actual data feed for TreeMap function for creating/drawing a node structure in UI
function createNode(obj, childObj) {
	var tempObj = {};
	switch (childObj.name) {

		case "Say":
			tempObj = {
				"HTMLid": childObj.id,
				"text": {
					"name": childObj.name,
					"nodeName": childObj.nodeName
				},
				"stackChildren": true,
				"children": []
			}
			break;
		case "Queue":
			tempObj = {
				"HTMLid": childObj.id,
				"text": {
					"name": childObj.name,
					"nodeName": childObj.nodeName
				},
				"stackChildren": true,
				"children": []
			}
			break;
		case "Dial":
			tempObj = {
				"HTMLid": childObj.id,
				"text": {
					"name": childObj.name,
					"nodeName": childObj.nodeName
				},
				"stackChildren": true,
				"children": []
			}
			break;
		case "Hangup":
			tempObj = {
				"HTMLid": childObj.id,
				"text": {
					"name": childObj.name,
					"nodeName": childObj.nodeName
				},
				"stackChildren": true,
				"children": []
			}
			break;
		case "Gather":
			tempObj = {
				"HTMLid": childObj.id,
				"text": {
					"name": childObj.name,
					"nodeName": childObj.nodeName

				},
				"stackChildren": true,
				"children": []
			}

			break;
		case "Digit":
			tempObj = {
				"HTMLid": childObj.id,
				"text": {
					"name": childObj.name,
					"nodeName": childObj.nodeName

				},
				"stackChildren": true,
				"children": []
			}

			break;
	}
	obj.push(tempObj);
}


//utility to truncate the characters upto length specified in check (second) parameter
function truncateValue(val, check) {
	if (!check)
		return val;
	if (val !== undefined && val.length > 24)
		return val.substr(0, 20) + "...";
	else
		return val;

}

//Delete node
function deleteNode() {

	for (var i = 1; i < IVRData.length; i++) {
		if (IVRData[i].id == +$(selectNode).attr("id") || IVRData[i].parent == +$(selectNode).attr("id")) {
			IVRData.splice(i, 1);
			i--;
		}
	}
}


function reset() {
	$('.addWindow').hide();
	$("#addAgentModalLabel").text("Select Action to perform");
	$('#nodeSelect').prop('selectedIndex', 0);
	$("textarea[name=say-content-text]").val('');
	$('#say-name').val('');
	$('#hangup-name').val('');
	$('#queue-content').val('');
	$('#queue-name').val('');
	$('#select-container-say').hide();
	$('#select-container-hangup').hide();
	$('#select-container-gather').hide();
	$('#select-container-queue').hide();
	$('#select-container-dial').hide();
	$('.deleteWindow').hide();
	$('#edit-btn').hide();
	$('#save-btn').hide();
	$('#delete-btn').hide();
	$("input[id=gather-name]").val("");
	$('#select-gather-nodes').val("");
	$('#select-gather-nodes').prop('selectedIndex', 0);
	$('#select-gather-nodes-div-container').empty();
	$('button#addBtn').prop('disabled', false);
	$('button#editBtn').prop('disabled', false);
	$('button#deleteBtn').prop('disabled', false);
	$('#goto-nodes-div-container').empty().hide();
	$('#dial-name').val('');
	$("#dial-content").val('');
	$("textarea[name=dial-content-text]").val('');
	$("textarea[name=gather-say-content-text]").val('');
	console.log(JSON.stringify(IVRData));
}



function drawLine() {

	setTimeout(function () {

		jsPlumb.ready(function () {
			jsPlumb.reset();
		});

		for (var i = 0; i < GOTOData.length; i++) {

			var firstElem = GOTOData[i].split("-")[0];
			var secondElem = GOTOData[i].split("-")[1];

			jsPlumb.ready(function () {
				jsPlumb.connect({
					//connector: ["Straight"],
					connector: ["Flowchart",
						{
							cornerRadius: 10,
							stub: 16
						}
					],
					overlays: [["Arrow", { location: 1, width: 10, length: 10 }]],
					source: firstElem,
					target: secondElem,
					anchor: ["Left", "Right"],
					endpoint: "Blank"
				});
			});


		}


	}, 500);


}



function createDigitContainer() {

	if ($('#select-gather-nodes').val() != null && $('#select-gather-nodes').val() != undefined) {

		var innerHTML = '';

		for (var i = 0; i < +$('#select-gather-nodes').val(); i++) {
			innerHTML += '<div class="row g-3 align-items-center selected-gather-digits">'
			for (var j = 0; j < main_item["Digit"].param.length; j++) {
				innerHTML += '<div class="col-auto input-digits-value"><label for="digit" class="col-form-label">' + (i + 1) + ':</label></div>'
				innerHTML += '<div class="col-auto input-digits-value"><input type="text" name="digit-name" class="form-control" id="digit-name" placeholder="Enter node name" value=""/></div>';
				innerHTML += '<div class="col-auto input-digits-value"><input type="' + main_item["Digit"].param[j].type + '" min="0" name="digit" class="form-control" id="digit" placeholder="' + main_item["Digit"].param[j].name + '" value=""/></div>';
			}
			innerHTML += '</div>';
		}
		$('#select-gather-nodes-div-container').empty().append(innerHTML).show();
	}
}

var main_item = {
	"Digit": {
		"description": "name",
		"param": [{
			name: "digit",
			type: "number"
		}],
		"showdropdown": true
	}
}