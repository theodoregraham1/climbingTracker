function open_username_editing() {
	document.getElementById("change-username-btn").style.display = "none";
	document.getElementById("change-username-li").innerHTML += `
		<form id="edit-username-form" name="edit-username-form">
			<input id="new-username" name="new-username" class="form-control mt-3" type="text" placeholder="New Username">
			<input id="password" name="password" class="form-control mt-3" type="password" placeholder="Password">
			<button class="btn btn-primary mt-3" type="submit" onclick="{edit_username(); return false;}">Change Username</button>
		</form>
	` // FIXME This resets the value of the disabled old-username element for no reason
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
			if (json["success"]) {
				close_editing_form("username");
			}

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
			<button class="btn btn-primary mt-3" type="submit" onclick="{edit_password(); return false;}">Change Password</button>
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
			}
			display_message(json["message"]["message"], json["message"]["tag"])
		})
	return false;
}


function open_image_editing() {
	document.getElementById("change-image-btn").style.display = "none";
	document.getElementById("change-image-li").innerHTML += `
		<form id="edit-image-form" name="edit-image-form">
			<input id="new-image" class="form-control mt-3" type="file">
			<button class="btn btn-primary mt-3" type="submit" onclick="{edit_image(); return false;}">Change Image</button>
		</form>
	`
	document.getElementById("edit-image-form")
		.addEventListener("submit", (event) => event.preventDefault())
}

function edit_image() {
	const data = new FormData()
	data.append("csrfmiddlewaretoken", get_CSRF_token())
	data.append("new-image", document.getElementById("new-image").files[0])

	data.forEach((item) => console.log(item))

	fetch(`../api/edit/image`, {
		method: "POST",
		body: data
	})
		.then(response => response.json())
		.then(json => {
			if (json["success"]) {
				close_editing_form("image");
			}
			document.getElementById(`old-image`).value = json[name];
			display_message(json["message"]["message"], json["message"]["tag"])
		})
}

function open_attr_editing(name) {
	document.getElementById(`change-${name}-btn`).style.display = "none";
	document.getElementById(`change-${name}-li`).innerHTML += `
		<form id="edit-${name}-form" name="edit-${name}-form">
			<input id="new-${name}" name="new-${name}" class="form-control mt-3" type="text" placeholder="New ${toCapitalised(name)}">
			<button class="btn btn-primary mt-3" type="submit" onclick="{edit_attribute('${name}'); return false;}">Change ${toCapitalised(name)}</button>
		</form>
	`
	document.getElementById(`edit-${name}-form`)
		.addEventListener("submit", (event) => event.preventDefault())
}

function edit_attribute(name) {
	const data = new FormData(document.forms.namedItem(`edit-${name}-form`));
	data.append("csrfmiddlewaretoken", get_CSRF_token())
	fetch(`../api/edit/${name}`, {
		method: "POST",
		body: data
	})
		.then(response => response.json())
		.then(json => {
			if (json["success"]) {
				close_editing_form(name);
			}
			document.getElementById(`old-${name}`).value = json[name];
			display_message(json["message"]["message"], json["message"]["tag"])
		})
	return false;
}

function open_add_setter_form() {
	document.getElementById(`add-setter-btn`).style.display = "none";
	document.getElementById(`setters-list`).innerHTML += `
		<form id="add-setter-form" name="add-setter-form" class="input-group">
				<input id="new-setter" name="new-setter" type="text" class="form-control" placeholder="New Setter" aria-describedby="add-setter-submit">
				<button class="btn btn-outline-primary" type="submit" id="add-setter-submit" onclick="{add_setter(); return false}">Add Setter</button>
		</form>
	`
	document.getElementById("add-setter-form")
		.addEventListener("submit", (event) => event.preventDefault())
}

function add_setter() {
	const data = new FormData(document.forms.namedItem(`add-setter-form`));
	data.append("csrfmiddlewaretoken", get_CSRF_token())
	data.append("action", "add")

	fetch(`../api/edit/setters`, {
		method: "POST",
		body: data
	})
		.then(response => response.json())
		.then(json => {
			if (json["success"]) {
				document.getElementById(`add-setter-btn`).style.display = "block";
				document.getElementById(`add-setter-form`).remove();
				document.getElementById('add-setter-btn').insertAdjacentHTML("beforebegin", `
					<li id="setter-${ json['id'] }-li" class="list-group-item form-group">
                        <span id="setter-${json['id']}" aria-describedby="setter-${json['id']}-remove-btn">${ json["username"]}</span>
                        <span class="badge text-bg-secondary interactable" id="setter-${json['id']}-remove-btn" onclick="remove_setter(${json['id']})">Remove Setter</span>
                    </li>
				`)
			}
			display_message(json["message"]["message"], json["message"]["tag"])
		})
	return false;
}

function remove_setter(id) {
	const data = new FormData()
	data.append("csrfmiddlewaretoken", get_CSRF_token())
	data.append("action", "remove")
	data.append("id", id)

	fetch(`../api/edit/setters`, {
		method: "POST",
		body: data
	})
		.then(response => response.json())
		.then(json => {
			if (json["success"]) {
				document.getElementById(`setter-${id}-li`).style.display = "None";
			}
			display_message(json["message"]["message"], json["message"]["tag"])
		})
}

function open_add_wall_form() {
	document.getElementById(`add-wall-btn`).style.display = "none";
	document.getElementById(`walls-list`).innerHTML += `
		<form id="add-wall-form" name="add-wall-form" class="input-group" action="/centres/walls/add" method="post">
				<input id="new-wall" name="new-wall" type="text" class="form-control" placeholder="New wall name" aria-describedby="add-wall-submit">
				<button class="btn btn-outline-primary" type="submit" id="add-wall-submit">Add Wall</button>
		</form>
	`
}
function close_editing_form(name) {
	document.getElementById(`change-${name}-btn`).style.display = "block";
	document.getElementById(`edit-${name}-form`).remove();
}
