// good old obtrusive JavaScript
function menuOpen() {
	var el = document.querySelector("header");
	if(el.classList.contains("open")) {
		el.classList.remove("open");
	} else {
		el.classList.add("open");
	}
}

window.onload = function() {
	var deeplinks = document.querySelectorAll("h2[id]");
	deeplinks.forEach(function(i) {
		i.innerHTML = '<a href="#' + i.id + '">' + i.innerHTML + "</a>";
	});
};
