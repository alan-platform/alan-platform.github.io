// The Alan language for Prism, which highlights the code blocks in the browser (layouts/partials/scripts.html loads
// this after Prism). It colours tokens by their kind, not by lists of words: in Alan a name is always quoted, so every
// bare word is a keyword of the language, an annotation such as @identifying included. The kinds: comments, text in
// double quotes, names in single quotes, numbers, keywords, and the symbols, the steps and operators of navigation and
// expressions (. > ^ => ~> = +) apart from the brackets, colons and commas that structure a model.
// The fences of the site are marked js, as the generator of the documentation writes them, and hold Alan:
// layouts/_markup/render-codeblock.html gives them the language alan.
(function(Prism) {
    Prism.languages.alan = {
        'comment': [
            {pattern: /\/\*[\s\S]*?\*\//, greedy: true},
            {pattern: /\/\/.*/, greedy: true}
        ],
        'string': {pattern: /"(?:\\.|[^"\\\r\n])*"/, greedy: true},
        'name': {pattern: /'(?:\\.|[^'\\\r\n])*'/, greedy: true},
        'number': /\b\d+(?:\.\d+)?\b/,
        'keyword': /@?[A-Za-z_][\w-]*/,
        'punctuation': /[[\]{}():,]/,
        'operator': /[^\s\w'"[\]{}():,]+/
    };
})(Prism);
