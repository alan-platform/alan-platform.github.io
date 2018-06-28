// good old obtrusive JavaScript
function menuOpen() {
	var el = document.querySelector("header");
	el.classList.toggle("open");
}

window.onload = function() {
	var deeplinks = document.querySelectorAll("h2[id], h3[id]");
	deeplinks.forEach(function(i) {
		i.innerHTML = '<a href="#' + i.id + '">' + i.innerHTML + "</a>";
	});

	var wide_switch = document.getElementById("wide");
	if (wide_switch) {
		wide_switch.onchange = function() {
			document.querySelector("article").classList.toggle("wide");
		};
	}
};
