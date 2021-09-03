// good old obtrusive JavaScript
// eslint-disable-next-line no-unused-vars
function menuOpen() {
    var el = document.querySelector('header');
    el.classList.toggle('open');
}

window.addEventListener('scroll', function() {
    if (window.scrollY > 0) {
        document.querySelector('header').classList.add('scrolled');
    } else {
        document.querySelector('header').classList.remove('scrolled');
    }
});

window.onload = function() {
    var deeplinks = document.querySelectorAll('h2[id], h3[id]');
    deeplinks.forEach(function(i) {
        i.innerHTML = '<a href="#' + i.id + '">' + i.innerHTML + '</a>';
    });

    document.querySelectorAll('pre code').forEach(function(element) {
        element.onclick = function() {
            var selection = window.getSelection();
            var range = document.createRange();
            range.selectNodeContents(element);
            selection.removeAllRanges();
            selection.addRange(range);
        };
    });


    var doc_menu_button = document.querySelector('[aria-controls="doc-list"]');
    if (doc_menu_button) {
        var doc_menu = document.getElementById(doc_menu_button.getAttribute('aria-controls'));
        doc_menu_button.onclick = function(event) {
            event.stopPropagation();
            if (doc_menu.getAttribute('aria-expanded') === 'false') {
                doc_menu.setAttribute('aria-expanded', 'true');
                doc_menu_button.setAttribute('aria-expanded', 'true');
            } else {
                doc_menu.setAttribute('aria-expanded', 'false');
                doc_menu_button.setAttribute('aria-expanded', 'false');
            }
        };
        document.body.addEventListener('click', function() {
            doc_menu.ariaExpanded = 'false';
            doc_menu_button.ariaExpanded = 'false';
        });
    }

    document.querySelectorAll('pre.code-custom').forEach(function(block) {
        var button = document.createElement('a');
        button.href = "/pages/tuts/syntax.html"
        button.classList.add('grammar-button');
        button.innerText = 'Grammar';
        button.title = "Go to grammar guide"
        block.appendChild(button);
    });
};
