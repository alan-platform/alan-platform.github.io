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

	document.querySelectorAll("pre code").forEach(function(element) {
		element.onclick = function() {
			var selection = window.getSelection();
			var range = document.createRange();
			range.selectNodeContents(element);
			selection.removeAllRanges();
			selection.addRange(range);
		};
	});

};
