function open_username_editing() {
	document.getElementById("change-username-btn").style.display = "none";
	document.getElementById("change-username-li").innerHTML += `
		<input id="new-username" name="new-username" class="form-control mt-3" type="text" placeholder="New Username">
		<input id="password" name="password" class="form-control mt-3" type="password" placeholder="Password">
		<button class="btn btn-primary mt-3">Change Username</button>
	` // TODO: Form submission
}