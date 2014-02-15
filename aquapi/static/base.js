// AquaPi Base JavaScript Library

// pnotify options
$.pnotify.defaults.styling = "jqueryui";
$.pnotify.defaults.maxonscreen = 5;
$.pnotify.defaults.nonblock: true;

// show pnotify window
function flashMessage(message) {
	$.pnotify({
		title: "Notification",
	       	text: message
	})
};
