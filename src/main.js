// The menu of the site header under 64rem. The toggle shows and hides it, and its aria-expanded says which: the
// stylesheet hides the menu while it is false. Escape closes the open menu and puts the focus back on the toggle,
// when the focus is in the header or nowhere; a key pressed elsewhere on the page is not the menu's. Without
// JavaScript the menu is always shown and the toggle is not (50-header.css).
function siteMenu() {
    var toggle = document.querySelector('.site-header .nav-toggle');
    if (!toggle) {
        return;
    }
    var header = toggle.closest('.site-header');
    function expand(open) {
        toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    }
    toggle.addEventListener('click', function() {
        expand(toggle.getAttribute('aria-expanded') !== 'true');
    });
    document.addEventListener('keydown', function(event) {
        if (event.key !== 'Escape' || toggle.getAttribute('aria-expanded') !== 'true') {
            return;
        }
        var focus = document.activeElement;
        if (focus && focus !== document.body && !header.contains(focus)) {
            return;
        }
        expand(false);
        toggle.focus();
    });
}
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', siteMenu);
} else {
    siteMenu();
}

// The page index (page-index.html): beside the content from 64rem, above it under 64rem. Under 64rem the label
// opens and closes the index; the rail marks the section in view. The layout builds the index from the headings of
// the page, so nothing here changes the layout of the page beyond opening and closing it.
function pageIndex() {
    var rail = document.querySelector('.page-index nav');
    var list = rail && rail.querySelector('#markdown-toc');
    if (!list) {
        return;
    }
    var index = rail.parentNode;
    var wide = window.matchMedia('(min-width: 64rem)');

    // Under 64rem the label is the control of a disclosure, closed at first. The stylesheet hides the list of a
    // closed index where the browser runs scripts, (scripting: enabled), before this runs; a browser that does not
    // know that feature keeps the list open, and gets no control here. The button takes the text of the label,
    // and is in the label only under 64rem: from there the label is a heading of the rail again, not a control.
    var label = index.querySelector('.page-index-label');
    if (label && window.matchMedia('(scripting: enabled)').matches) {
        var toggle = document.createElement('button');
        toggle.type = 'button';
        toggle.className = 'page-index-toggle';
        toggle.setAttribute('aria-controls', list.id);
        toggle.setAttribute('aria-expanded', 'false');
        toggle.textContent = label.textContent;
        var setOpen = function(open) {
            index.classList.toggle('page-index-open', open);
            toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
        };
        toggle.addEventListener('click', function() {
            setOpen(!index.classList.contains('page-index-open'));
        });
        var layout = function() {
            if (wide.matches) {
                if (toggle.parentNode) {
                    label.textContent = toggle.textContent;
                }
            } else if (!toggle.parentNode) {
                label.textContent = '';
                label.appendChild(toggle);
                // a link that has the focus when the window becomes narrow stays in view
                if (list.contains(document.activeElement)) {
                    setOpen(true);
                }
            }
        };
        layout();
        wide.addEventListener('change', layout);
    }

    // follow exactly the entries the index shows: heading levels differ per page, and the generated
    // grammars skip levels (an h2 section with h5 subsections), so a fixed list of tags misses sections.
    // The stylesheet shows two levels; an entry of the third (li li li) is left out.
    var links = {};
    var headings = [];
    list.querySelectorAll('a[href^="#"]').forEach(function(link) {
        if (link.closest('li li li')) {
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

        // a long rail scrolls on its own; keep the marked entry in view without moving the page
        if (index.scrollHeight > index.clientHeight) {
            var top = link.getBoundingClientRect().top - index.getBoundingClientRect().top;
            if (top < 0 || top + link.offsetHeight > index.clientHeight) {
                index.scrollTop += top - (index.clientHeight - link.offsetHeight) / 2;
            }
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

    // The line where a jump puts a heading: the bottom of the site header, which sticks to the top of the window
    // or has scrolled out of it on a low window, and the 24px (1.5rem) that the stylesheet keeps between the two.
    // The header is measured, not taken from the stylesheet: it grows when the text is enlarged.
    var header = document.querySelector('body > header');
    function line() {
        var bottom = header ? Math.max(header.getBoundingClientRect().bottom, 0) : 0;
        return bottom + 1.5 * parseFloat(getComputedStyle(document.documentElement).fontSize);
    }

    // the reader is in the section of the last heading that reached that line, or in the last section once the
    // page is scrolled to its end
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
        var limit = line() + 1;
        var heading = headings[0];
        for (var i = 0; i < headings.length; i++) {
            if (headings[i].getBoundingClientRect().top > limit) {
                break;
            }
            heading = headings[i];
        }
        if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2) {
            heading = headings[headings.length - 1];
        }
        mark(heading);
    }

    list.addEventListener('click', function(event) {
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

// Release notes put the code that illustrates an item straight after the list, so it renders outside it: the code
// moves into the last item, with what follows it up to the next list or heading. This runs as soon as the document
// is parsed, before the first paint where it can, so that the code does not visibly jump.
function releaseNotesCode() {
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
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', releaseNotesCode);
    document.addEventListener('DOMContentLoaded', markCurrentDocument);
    document.addEventListener('DOMContentLoaded', documentSwitch);
} else {
    releaseNotesCode();
    markCurrentDocument();
    documentSwitch();
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
