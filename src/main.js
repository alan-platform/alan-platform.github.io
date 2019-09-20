// good old obtrusive JavaScript
// eslint-disable-next-line no-unused-vars
function menuOpen() {
    var el = document.querySelector('header');
    el.classList.toggle('open');
}

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
    var doc_menu = document.getElementById(doc_menu_button.ariaControls);
    doc_menu_button.onclick = function(event) {
        event.stopPropagation();
        if (doc_menu.ariaExpanded === 'false') {
            doc_menu.ariaExpanded = 'true';
            doc_menu_button.ariaExpanded = 'true';
        } else {
            doc_menu.ariaExpanded = 'false';
            doc_menu_button.ariaExpanded = 'false';
        }
    };
    document.body.addEventListener('click', function() {
        doc_menu.ariaExpanded = 'false';
        doc_menu_button.ariaExpanded = 'false';
    });


    document.querySelectorAll('div.highlight').forEach(function(block) {
        if (block.scrollHeight > block.offsetHeight) {
            // it has a scrollbar

            var button = document.createElement('button');
            button.classList.add('expand-button');
            button.innerText = 'Expand';

            button.onclick = function() {
                block.classList.add('expanded');
                button.remove();
            };

            block.appendChild(button);
        }
    });


};
