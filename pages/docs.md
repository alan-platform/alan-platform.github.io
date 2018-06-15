---
layout: page
title: Docs
category: main
permalink: /docs/
---

- Some basic documentation about [how to use Alan](/pages/tuts/readme.html).
- A tutorial for [creating data migrations](/pages/tuts/migration.html).
- A tutorial on how to build your first application (coming soon!).

Don't be afraid to ask questions [on StackOverflow](https://stackoverflow.com/questions/tagged/alan) (use the `#alan` tag)!



## How to read grammars

- Keywords are between `[]`, e.g. `'state group' [ '?' ] reference`.
- `component 'some component'` refers to a different component in the same language.

## Typical quirks of the Alan compiler

- Keywords should be separated by whitespace, so `()` doesn't work but `( )` does. 
- Quotes are recognized as something special, so you *can* write `'type':` and `?'state group'|'state'`.
- Single quotes are used for entities (things you can refer to or that refer to something else), double quotes are just strings.
- Only tabs are accepted for indentation.


## Important languages:

{% include doc-index.html %}



## Alan and Windows
Alan is built to run in a Unix-like environment. We rely on tools like bash and curl that are native to Linux and macOS. 

On Windows you can use the MinGW terminal (aka. Git Bash) provided by [Git-For-Windows](https://gitforwindows.org). Using our Linux builds in WSL or a Linux VM are also possible.

The Alan Application Server only runs on a "real" POSIX system. Run it in WSL under the Linux filesystem, or a VM or external Linux server.



## Editor support 

- Sublime Text 3: install "Alan" via [Package Control](https://packagecontrol.io/packages/Alan)
- VS Code: install "Alan" from [the Marketplace](https://marketplace.visualstudio.com/items?itemName=M-industries.alan)
- VIM: download [AlanForVim](https://github.com/M-industries/AlanForVim/archive/master.zip)
- Emacs: install [AlanForEmacs](https://github.com/M-industries/AlanForEmacs)
- Atom: install [language-alan](https://atom.io/packages/language-alan)
