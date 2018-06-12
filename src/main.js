// good old obtrusive JavaScript
function menuOpen() {
	var el = document.querySelector("header");
	if(el.classList.contains("open")) {
		el.classList.remove("open");
	} else {
		el.classList.add("open");
	}
}
