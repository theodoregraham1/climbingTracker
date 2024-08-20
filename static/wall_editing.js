let selected_new_grades = []
let selected_edit_grades = []

editing = false

function add_route() {
	if (selected_new_grades.length === 0) {
		return false;
	}

	const data = new FormData();

	data.append("csrfmiddlewaretoken", get_CSRF_token());

	let gradesString = selected_new_grades[0];
	for (let i = 1; i < selected_new_grades.length ; i++) {
		gradesString += "," + selected_new_grades[i]
	}

	data.append("grades", gradesString);
	data.append("number", document.getElementById("new-route-number").value)
	data.append("wall", wall_id)

	fetch(`../../../api/walls/add-route`, {
		method: "POST",
		body: data
	})
}

function add_new_grade() {
	const grade = document.getElementById("new-route-grades").value;

	if (grade == 0) {
		return;
	} else if (selected_new_grades.length == 0) {
		document.getElementById("selected-grades-div").innerHTML = `
			<ul class="list-group pb-3" id="selected-grades">
			</ul>
		`
	}

	document.getElementById("selected-grades").innerHTML += `
		<li class="list-group-item">
			${grade}
		</li>
	`;
	selected_new_grades.push(grade);
}

function open_edit_route(id) {
	if (editing) {
		document.getElementById(`route-${id}-edit-btn`).disable()
	}

	editing = true

	const edit_btn = document.getElementById(`route-${id}-edit-btn`)
	edit_btn.innerText = "Complete edit"
	edit_btn.onclick = function () {complete_route_edit(id)}
	edit_btn.classList = "btn btn-primary"

	document.getElementById(`route-${id}-grades`).innerHTML = `
		<div class="input-group col-md-9 my-3">
			<label class="input-group-text" for="route-${id}-edit-grades">Select grades</label>
	        <select id="route-${id}-edit-grades" class="form-select">
	            <option selected disabled value="0">Select grades</option>
	        </select>
	        <button class="btn btn-secondary" type="reset" onclick="add_edit_grade(${id})">Add grade</button>
        </div>
        
        <div id="edit-grades-div"></div>
	`
	POSSIBLE_GRADES.forEach((grade) => {
		document.getElementById(`route-${id}-edit-grades`).innerHTML += `
			<option value="${grade}">${grade}</option>
		`
	})
}

function add_edit_grade(id) {
	const grade = document.getElementById(`route-${id}-edit-grades`).value;

	if (grade == 0) {
		return;
	} else if (selected_edit_grades.length == 0) {
		document.getElementById("edit-grades-div").innerHTML = `
			<ul class="list-group pb-3" id="edit-selected-grades">
			</ul>
		`
	}

	document.getElementById("edit-selected-grades").innerHTML += `
		<li class="list-group-item">
			${grade}
		</li>
	`;
	selected_edit_grades.push(grade);
}

function complete_route_edit(id) {
	if (selected_edit_grades.length === 0) {
		return false;
	}

	const data = new FormData();

	data.append("csrfmiddlewaretoken", get_CSRF_token());

	let gradesString = selected_edit_grades[0];
	for (let i = 1; i < selected_edit_grades.length ; i++) {
		gradesString += "," + selected_edit_grades[i]
	}

	data.append("grades", gradesString);
	data.append("wall", wall_id)

	fetch(`../../../api/walls/edit-route/${id}`, {
		method: "POST",
		body: data
	})

	location.reload()
}
