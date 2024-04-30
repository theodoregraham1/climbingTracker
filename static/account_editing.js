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

function close_username_editing() {
	document.getElementById("change-username-btn").style.display = "block";
	document.getElementById("edit-username-form").remove();
}

function edit_username() {
	const data = new FormData(document.forms.namedItem("edit-username-form"));
	data.append("csrfmiddlewaretoken", document.getElementsByName("csrfmiddlewaretoken")[0].value)

	fetch(`../api/edit/username`, {
		method: "POST",
		body: data
	})
		.then(response => response.json())
		.then(json => {
			document.getElementById("old-username").value = json["username"];
			document.getElementById("username-link").innerText = json["username"]
			close_username_editing();
		})
	return false;
}

//TODO Allow dynamic updating of messages