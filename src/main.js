// good old obtrusive JavaScript
// eslint-disable-next-line no-unused-vars
function menuOpen(button) {
    var el = document.querySelector('header');
    var open = el.classList.toggle('open');
    if (button) {
        button.setAttribute('aria-expanded', open ? 'true' : 'false');
    }
}

// Marks the section in view in the rail beside the content. The layout builds the rail from the headings of
// the page (page-index.html), so nothing here changes the layout of the page.
function pageIndex() {
    var rail = document.querySelector('.page-index nav');
    if (!rail || !rail.querySelector('#markdown-toc')) {
        return;
    }

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

    // A section the reader jumped to (an entry of the index, or any link to its heading) stays marked while its
    // heading is on screen: the last sections of a page cannot scroll up to the top, so the rule below would
    // never reach them. Until the jump has arrived, the scrolling it causes does not count.
    var pinned = null;
    var arrived = false;
    function pin(id) {
        var heading = document.getElementById(id);
        if (!heading || !links[heading.id]) {
            return;
        }
        pinned = heading;
        arrived = false;
        mark(heading);
    }

    // the reader is in the section of the last heading that passed under the fixed header, or in the last section
    // once the page is scrolled to its end
    function follow() {
        if (pinned) {
            var top = pinned.getBoundingClientRect().top;
            if (top >= 0 && top < window.innerHeight) {
                arrived = true;
                mark(pinned);
                return;
            }
            if (!arrived) {
                return;
            }
            pinned = null;
        }
        var heading = headings[0];
        for (var i = 0; i < headings.length; i++) {
            if (headings[i].getBoundingClientRect().top > 96) {
                break;
            }
            heading = headings[i];
        }
        if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2) {
            heading = headings[headings.length - 1];
        }
        mark(heading);
    }

    rail.addEventListener('click', function(event) {
        var link = event.target.closest('a[href^="#"]');
        if (link) {
            pin(decodeURIComponent(link.getAttribute('href').substring(1)));
        }
    });
    window.addEventListener('hashchange', function() {
        pin(decodeURIComponent(location.hash.substring(1)));
    });
    if (location.hash) {
        pin(decodeURIComponent(location.hash.substring(1)));
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

// as soon as the document is parsed: waiting for the images would leave the rail unmarked for a while
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', pageIndex);
} else {
    pageIndex();
}

// The archive lists a section per platform version, the table of the stable one open. A link that names a
// version in the fragment (/docs/archive#2026.3) opens the table of that section and closes the others, so the
// reader lands on the version the link is about; the browser scrolls to it as to any fragment.
function archiveVersion() {
    if (!location.hash) {
        return;
    }
    var target = document.getElementById(decodeURIComponent(location.hash.substring(1)));
    if (!target || !target.matches('.archive-version')) {
        return;
    }
    document.querySelectorAll('.archive-version').forEach(function(section) {
        section.querySelector('details').open = section === target;
    });
}
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', archiveVersion);
} else {
    archiveVersion();
}
window.addEventListener('hashchange', archiveVersion);

// The documentation tables are rendered once per version (partialCached), so the link of the current page is marked
// here, and its row, before the reader can open the "Switch document" table.
function markCurrentDocument() {
    document.querySelectorAll('.doc-table a').forEach(function(link) {
        if (link.pathname === location.pathname) {
            link.setAttribute('aria-current', 'page');
            var row = link.closest('tbody tr');
            if (row) {
                row.classList.add('current');
            }
        }
    });
}

// "Switch document" on a documentation page: a button that shows and hides the language table under the header, a
// disclosure (aria-expanded on the button, hidden on the table), not a menu: Tab moves through its links as through
// the page. Escape closes it, and returns the focus to the button when it was in the table. From 40rem the table
// opens over the document (70-docs.css): there a click outside it closes it, and so does the focus leaving it and the
// button, so that it never covers the link that has the focus; it is as high as the window leaves under it, less 16px
// of air, and at least 240px. Under 40rem it is in the flow of the page and stays open until the button closes it.
function documentSwitch() {
    var button = document.querySelector('[aria-controls="doc-list"]');
    if (!button) {
        return;
    }
    var list = document.getElementById(button.getAttribute('aria-controls'));
    var over = window.matchMedia('(min-width: 40rem)');

    function fit() {
        var room = window.innerHeight - list.getBoundingClientRect().top - 16;
        list.style.setProperty('--doc-list-height', Math.max(room, 240) + 'px');
    }

    function show(open) {
        button.setAttribute('aria-expanded', open ? 'true' : 'false');
        list.hidden = !open;
        if (open) {
            list.scrollTop = 0;
            fit();
        }
    }

    button.addEventListener('click', function() {
        show(list.hidden);
    });
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && !list.hidden) {
            var inside = list.contains(document.activeElement);
            show(false);
            if (inside) {
                button.focus();
            }
        }
    });
    document.addEventListener('click', function(event) {
        if (!list.hidden && over.matches && !list.contains(event.target) && !button.contains(event.target)) {
            show(false);
        }
    });
    // a click on the panel itself moves the focus nowhere (relatedTarget null): that is not leaving it
    function leave(event) {
        var to = event.relatedTarget;
        if (!list.hidden && over.matches && to && to !== button && !list.contains(to)) {
            show(false);
        }
    }
    button.addEventListener('focusout', leave);
    list.addEventListener('focusout', leave);
    window.addEventListener('resize', function() {
        if (!list.hidden) {
            fit();
        }
    });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', markCurrentDocument);
    document.addEventListener('DOMContentLoaded', documentSwitch);
} else {
    markCurrentDocument();
    documentSwitch();
}

window.addEventListener('scroll', function() {
    if (window.scrollY > 0) {
        document.querySelector('header').classList.add('scrolled');
    } else {
        document.querySelector('header').classList.remove('scrolled');
    }
});

window.onload = function() {
    // release notes put the code that illustrates an item straight after the list, so it renders outside it;
    // move that code into the last item, with what follows it up to the next list or heading
    document.querySelectorAll('.release-notes section > ul').forEach(function(list) {
        var next = list.nextElementSibling;
        if (!next || !next.classList.contains('highlighter-rouge')) {
            return;
        }
        while (next && !next.matches('ul, ol, h1, h2, h3, h4, h5, h6, hr')) {
            var moving = next;
            next = next.nextElementSibling;
            list.lastElementChild.appendChild(moving);
        }
    });

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


    document.querySelectorAll('pre.code-custom').forEach(function(block) {
        var button = document.createElement('a');
        button.href = "/pages/tuts/syntax.html"
        button.classList.add('grammar-button');
        button.innerText = 'Grammar';
        button.title = "Go to grammar guide"
        block.appendChild(button);
    });

    // a code block marked {: .copy} in the markdown gets a button that copies its text
    document.querySelectorAll('.copy div.highlight').forEach(function(block) {
        var code = block.querySelector('code');
        var button = document.createElement('button');
        button.type = 'button';
        button.classList.add('copy-button');
        button.innerText = 'Copy';
        button.title = 'Copy to the clipboard';
        function copied() {
            button.innerText = 'Copied';
            setTimeout(function() {
                button.innerText = 'Copy';
            }, 1500);
        }
        // without the clipboard API (not a secure context) or when it refuses, copy the selection
        function copySelection() {
            var selection = window.getSelection();
            var range = document.createRange();
            range.selectNodeContents(code);
            selection.removeAllRanges();
            selection.addRange(range);
            if (document.execCommand('copy')) {
                copied();
            }
            selection.removeAllRanges();
        }
        button.onclick = function() {
            if (navigator.clipboard) {
                navigator.clipboard.writeText(code.innerText.replace(/\n$/, '')).then(copied, copySelection);
            } else {
                copySelection();
            }
        };
        block.appendChild(button);
    });
};
