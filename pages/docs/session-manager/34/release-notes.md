---
layout: "doc"
origin: "session-manager"
language: "release notes"
version: "34"
type: "release notes"
url: "/pages/docs/session-manager/34/release-notes.html"
---
## 34

- The session manager renders its login pages itself, with CSRF protection, and implements the OAuth2 authorization code flow. The stylesheet matches the webclient layout; on wide screens the form keeps its width. Pages carry a robots meta tag.
- A login with a temporary password now leads to the mandatory password change.
- Matching a URL against the whitelist ignores its fragment.
- A session lasts until its `'token limit'` or until logout; the idle timeout `'token interval'` no longer applies. Datastores report every token they hold as active, so it rarely ended a session anyway.
- Deploying with a `tokens.json` that holds sessions, such as one from a publish, no longer fails with "token key must be 63 bytes"; the check now uses the key size the session manager issues.
- Authentication domains: claim cycles, dropped domain clients and connection errors are handled more robustly.
- Builds for darwin-arm64.
- The package ships an agent guide (AGENTS.md).

`config.alan` is unchanged: there is nothing to upgrade by hand. `'token interval'` is still required, but its value is ignored.
