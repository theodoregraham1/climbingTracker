function open_username_editing() {
	document.getElementById("change-username-btn").style.display = "none";
	document.getElementById("change-username-li").innerHTML += `
		<form id="edit-username-form" name="edit-username-form">
			<input id="new-username" name="new-username" class="form-control mt-3" type="text" placeholder="New Username">
			<input id="password" name="password" class="form-control mt-3" type="password" placeholder="Password">
			<button class="btn btn-primary mt-3" type="submit" onclick="{edit_username(); return false;}">Change Username</button>
		</form>
	`
	document.getElementById("edit-username-form")
		.addEventListener("submit", (event) => event.preventDefault())
}

function edit_username() {
	const data = new FormData(document.forms.namedItem("edit-username-form"));
	data.append("csrfmiddlewaretoken", get_CSRF_token())

	fetch(`../api/edit/username`, {
		method: "POST",
		body: data
	})
		.then(response => response.json())
		.then(json => {
			document.getElementById("old-username").value = json["username"];
			document.getElementById("username-link").innerText = json["username"]
			close_editing_form("username");

			if (json["message"] != null) {
				display_message(json["message"]["message"], json["message"]["tag"])
			}
		})
	return false;
}


function open_password_editing() {
	document.getElementById("change-password-btn").style.display = "none";
	document.getElementById("change-password-li").innerHTML += `
		<form id="edit-password-form" name="edit-password-form">
			<input id="old-password" name="old-password" class="form-control mt-3" type="password" placeholder="Current Password">
			<input id="new-password" name="new-password" class="form-control mt-3" type="password" placeholder="New Password">
			<input id="confirmation" name="confirmation" class="form-control mt-3" type="password" placeholder="Retype New Password">
			<button class="btn btn-primary mt-3" type="submit" onclick="{edit_password(); return false;}">Change Username</button>
		</form>
	`
	document.getElementById("edit-password-form")
		.addEventListener("submit", (event) => event.preventDefault())
}

function edit_password() {
	const data = new FormData(document.forms.namedItem("edit-password-form"));
	data.append("csrfmiddlewaretoken", get_CSRF_token())

	fetch(`../api/edit/password`, {
		method: "POST",
		body: data
	})
		.then(response => response.json())
		.then(json => {
			if (json["success"]) {
				close_editing_form("password");
			} else {
				display_message(json["message"]["message"], json["message"]["tag"])
			}
		})
	return false;
}


function close_editing_form(name) {
	document.getElementById(`change-${name}-btn`).style.display = "block";
	document.getElementById(`edit-${name}-form`).remove();
}

//TODO Allow dynamic updating of messages