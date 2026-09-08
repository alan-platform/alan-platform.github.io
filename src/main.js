// good old obtrusive JavaScript
// eslint-disable-next-line no-unused-vars
function menuOpen() {
    var el = document.querySelector('header');
    el.classList.toggle('open');
}

// Moves the table of contents that kramdown emits into the rail beside the content, and marks the
// section in view. Pages without a table of contents keep an empty, hidden rail.
function pageIndex() {
    var list = document.getElementById('markdown-toc');
    var rail = document.querySelector('.page-index nav');
    if (!list || !rail) {
        return;
    }

    rail.appendChild(list);
    rail.parentNode.removeAttribute('hidden');
    document.querySelector('main').classList.add('has-page-index');


    // follow exactly the entries the index shows: heading levels differ per page, and the generated
    // grammars skip levels (an h2 section with h5 subsections), so a fixed list of tags misses sections
    var links = {};
    var headings = [];
    rail.querySelectorAll('a[href^="#"]').forEach(function(link) {
        if (link.offsetParent === null) { // a level the stylesheet hides
            return;
        }
        var heading = document.getElementById(decodeURIComponent(link.getAttribute('href').substring(1)));
        if (heading) {
            links[heading.id] = link;
            headings.push(heading);
        }
    });
    if (headings.length === 0) {
        return;
    }

    var current = null;
    function mark(heading) {
        if (current === heading) {
            return;
        }
        if (current) {
            links[current.id].removeAttribute('aria-current');
        }
        current = heading;
        var link = links[current.id];
        link.setAttribute('aria-current', 'location');

        // a long index scrolls on its own; keep the marked entry in view without moving the page
        var offset = link.offsetTop - rail.offsetTop;
        if (offset < rail.parentNode.scrollTop || offset > rail.parentNode.scrollTop + rail.parentNode.clientHeight - link.offsetHeight) {
            rail.parentNode.scrollTop = offset - rail.parentNode.clientHeight / 2;
        }
    }

    // the reader is in the section of the last heading that passed under the fixed header
    function follow() {
        var heading = headings[0];
        for (var i = 0; i < headings.length; i++) {
            if (headings[i].getBoundingClientRect().top > 96) {
                break;
            }
            heading = headings[i];
        }
        mark(heading);
    }

    var scheduled = false;
    window.addEventListener('scroll', function() {
        if (scheduled) {
            return;
        }
        scheduled = true;
        window.requestAnimationFrame(function() {
            scheduled = false;
            follow();
        });
    });
    follow();
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

    pageIndex();

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

    // the documentation tables are rendered once per version (include_cached), so mark the current page here
    document.querySelectorAll('table td > a').forEach(function(link) {
        if (link.pathname === location.pathname) {
            link.closest('tr').classList.add('current');
        }
    });

    document.querySelectorAll('pre.code-custom').forEach(function(block) {
        var button = document.createElement('a');
        button.href = "/pages/tuts/syntax.html"
        button.classList.add('grammar-button');
        button.innerText = 'Grammar';
        button.title = "Go to grammar guide"
        block.appendChild(button);
    });
};
