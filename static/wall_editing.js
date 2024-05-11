let selected_new_grades = []

function add_route() {

}

function add_grade() {
	if (selected_new_grades.length === 0) {
		document.getElementById("selected-grades-div").innerHTML = `
			<ul class="list-group" id="selected-grades">
			</ul>
		`
	}

	document.getElementById("selected-grades").innerHTML += `
		<li class="list-group-item">
			${document.getElementById("new-route-grades").value}
		</li>
	`


}