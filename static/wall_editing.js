let selected_new_grades = []

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

function add_grade() {
	const grade = document.getElementById("new-route-grades").value;

	if (grade == 0) {
		return;
	}
	if (selected_new_grades.length == 0) {
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
