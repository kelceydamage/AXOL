/**
 * Loads a response from a request into a target container
 * @param  {string} source The url to load
 * @param  {object||string} target The document object representing the container into which the 
 *                                 		response will be loaded or the id as a string
 */
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

			//Now we update the target with the response
			target.innerHTML = request.responseText;
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

/**
 * Reloads a targeted content section from an external source when the trigger is activated
 * @param  {string||array} targets  The id of the HTML element that should be loaded with new content
 *                                  	as a string or an array of strings
 * @param  {string} trigger The id of the HTML element that acts as a trigger on the click event
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
	trigger.onclick = function(event){

		//Prevent the default action of the trigger. This prevents links from being followed or forms from submitting
		//because we want to handle everything locally on the page
		event.preventDefault();
		
		//Iterate over each target
		var i = targets.length;
		while (i--){

			//For each target, call the load function
			load(sources[i], targets[i]);
		}
	}
};