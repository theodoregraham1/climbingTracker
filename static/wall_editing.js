let selected_new_grades = []

function add_route() {
	const data = new FormData();
	data.append("csrfmiddlewaretoken", get_CSRF_token());
	data.append("grades", JSON.stringify(selected_new_grades));
	data.append("number", document.getElementById("new-route-number").value)

	fetch(`../api/walls/${wall_id}/add-route`, {
		method: "POST",
		body: data
	})
		.then(response => response.json())
		.then(json => {
			if (json["success"]) {
				const number_input = document.getElementById("new-route-number");
				number_input.value += 1
			}
			display_message(json["message"]["message"], json["message"]["tag"])
		})
	return false;
}

function add_grade() {
	const grade = document.getElementById("new-route-grades").value;

	if (grade === 0) {
		return;
	}
	if (selected_new_grades.length === 0) {
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