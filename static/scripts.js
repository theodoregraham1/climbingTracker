function display_message(message, tag) {
	// Intentionally clears messages
	document.getElementById("messages-container").innerHTML = `
		<div class="alert alert-${tag}" role="alert">${message}</div>
	`
	console.log(`
		<div class="alert alert-${tag}" role="alert">${message}</div>
	`)
}

function get_CSRF_token() {
	return document.getElementsByName("csrfmiddlewaretoken")[0].value;
}
