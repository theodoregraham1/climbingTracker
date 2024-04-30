const PAGE_SIZE = 5;

let page_num = 0;

document.addEventListener("DOMContentLoaded", function () {
	if (page_num === 0) disable("page-previous-btn")
	load_page(page_num)
})

function load_page() {
	if (page_num === 0) disable("page-previous-btn")
	else activate("page-previous-btn")

	const data = new FormData();

	data.append("page_num", String(page_num),);
	data.append('page_size', String(PAGE_SIZE));
	data.append("csrfmiddlewaretoken", document.getElementsByName("csrfmiddlewaretoken")[0].value)

	fetch("api/centres", {
		method: "POST",
		body: data
	})
		.then(response => response.json())
		.then(centres => {
			clear("centres-display")
			if (centres.length < PAGE_SIZE) {
				disable("page-next-btn")
			} else {
				disable("page-next-btn")
			}

			centres.forEach(centre => add_centre(centre))
		})
}

function add_centre(centre) {
	const li = document.createElement("li")

	li.id = `centre-${centre.id}`
	li.className = "list-group-item mx-auto col-md-6 mt-3"
	li.innerHTML = ` 
			<h3><a href="#">${centre.name}</a></h3>
			<img src="${centre.image_url}" alt="Image provided by climbing centre ${centre.name}">
			<p>${centre.location}</p>
	`
	// TODO: Hyperlink for centre
	// TODO: Provide messages of recent activity from each

	document.getElementById("centres-display").append(li)
}

function disable(id) {
	let btn = document.getElementById(id);

	btn.disabled = true;
	btn.classList.add("disabled");
	btn.tabIndex = -1;
	btn.ariaDisabled = "true";

	console.log("Disabled button: ", id)
}

function activate(id) {
	let btn = document.getElementById(id);

	btn.disabled = false;
	btn.classList.remove("disabled");
	btn.tabIndex = 1;
	btn.ariaDisabled = "false";

	console.log("Activated button: ", id)
}

function clear(id) {
	document.getElementById(id).innerHTML = ``
}