---
layout: "doc"
origin: "session-manager"
language: "release notes"
version: "partitions-108.5"
type: "release notes"
---
## partitions-108.4.1 (after 33)

- The session manager renders its login pages itself, with CSRF protection, and implements the OAuth2 authorization code flow. The stylesheet matches the webclient layout; on wide screens the form keeps its width. Pages carry a robots meta tag.
- A login with a temporary password now leads to the mandatory password change.
- Matching a URL against the whitelist ignores its fragment.
- Authentication domains: claim cycles, dropped domain clients and connection errors are handled more robustly.
- Builds for darwin-arm64.
- The package ships an agent guide (AGENTS.md).

`config.alan` is unchanged: there is nothing to upgrade by hand.
