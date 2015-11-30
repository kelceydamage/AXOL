
/*var name = prompt('what is your name?', '');

var new_div = document.createElement('div');
new_div.id = 'block';
new_div.className = 'block';
var body = document.getElementsByTagName('body')[0];
body.appendChild(new_div);

var inner_div = document.createElement('div');
inner_div.className = 'block2';
inner_div.id = 'block2';
new_div.appendChild(inner_div);

var button1 = document.createElement('button');
button1.id = 'button1';
button1.value = 'Click';
new_div.appendChild(button1);
*/

var func1 = function(){
	var inner_div = document.getElementById('block2');
	//inner_div.setAttribute('data-source', 'http://54.201.119.11/api/heartbeat');
	inner_div.setAttribute('data-source', 'http://54.201.119.11/api/cpu/staging_web_servers');
};


/*new_div.getAttribute('data-source');
*/
/*new_div.data-source = 'http://54.201.119.11/api/cpu/';
*/
/*
var load = function(source, target){
	console.log(source);
	console.log(target);
	//target = document.getElementById('block2');
	//source = target.getAttribute('data-source');
	var request = new XMLHttpRequest();
	request.onreadystatechange = function(){
		if (request.readyState == 4){
			console.log(request.responseText)
			target.innerHTML = request.responseText;
		}
	};
	request.open('GET', source);
	request.responseType = 'text';
	request.send();
};
//*/

var load = function(source, target){
	//We need to check if the target is string and make it a document object if it is
	if (typeof target === 'string'){
		target = document.getElementById(target);
	}

	//The XMLHttpRequest object will handle our AJAX call. You can view more info on the object at:
	//https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest
	var request = new XMLHttpRequest();

	//First we need to tell it what to do when it successfully gets the file
	//We do this by listening for a change in the request object's readyState property
	//This function won't run until the request is sent
	request.onreadystatechange = function(){

		//A readyState of 4 means that the request is complete
		if (request.readyState == 4){

			console.log(source, request.responseText);
			//Now we update the target with the response
			target.innerHTML = request.responseText;
			console.log(target.innerHTML);
		}
	};

	//Now we set the HTTP method and target for the request
	request.open("GET", source);

	//The responseType must be text in this case because we're simply replacing the content
	//If you were to manipulate the response before updating the content, you would need to use
	//a different responseType
	request.responseType = "text";

	//And that's it!
	request.send();
};

/*document.addEventListener("DOMContentLoaded", function(){

load();

source = inner_div.getAttribute('data-source');
load(source, target);

});
*/
/*
var reload = function(){
	target = document.getElementById('block2');
	source = target.getAttribute('data-source');
	trigger = document.getElementById('button1');
	trigger.addEventListener('click', function(event){
		load();
	});
};
*/
var reload = function(targets, trigger){

	//Because the target can be a string or an array, we need to normalize its format by making any
	//string into an array
	if (typeof targets === 'string'){
		targets = [targets];
	}

	//We'll need a set of sources for each target, so we'll create an empty array for now
	var sources = [];

	//Because the targets is an array, we need to iterate over it to get each document object
	var numTargets = targets.length;
	while (numTargets--){

		//We'll replace each string id in the targets array with the document object representing
		//that id instead
		targets[numTargets] = document.getElementById(targets[numTargets]);

		//And set the corresponding source from the target's data-source attribute
		sources[numTargets] = targets[numTargets].getAttribute('data-source');
	}

	//Locate the trigger in the document by creating its document object
	trigger = document.getElementById(trigger);

	//Set up the on click event handler
	trigger.addEventListener('click', function(event){

		//Iterate over each target
		var i = targets.length;
		while (i--){

			//If the role exists, add it to the source
			//We have to do this here because the role may have changed since the last time the page was loaded
			//var source = (targets[i].getAttribute('data-role')) ? sources[i] + targets[i].getAttribute('data-role') : sources[i];
			//var source = 'http://54.201.119.11/api/heartbeat';
			var source = 'http://54.201.119.11/api/cpu/staging_web_servers';

			//For each target, call the load function
			load(source, targets[i]);
		}
	}, false);
};
