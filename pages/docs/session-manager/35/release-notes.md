---
layout: "doc"
origin: "session-manager"
language: "release notes"
version: "35"
type: "release notes"
---
## 35

35 supersedes 34, which is withdrawn: do not deploy 34. The changes below are relative to 33.

- The session manager renders its login pages itself, with CSRF protection, and implements the OAuth2 authorization code flow. The stylesheet matches the webclient layout; on wide screens the form keeps its width. Pages carry a robots meta tag.
- An OpenID login now redirects to `<base uri>oidc/resume` instead of the base uri itself: register that address with the client at the provider (Google, Entra) before an application moves to 35, or the provider refuses the login (Google with `redirect_uri_mismatch`).
- A login with a temporary password now leads to the mandatory password change.
- Matching a URL against the whitelist ignores its fragment.
- A session lasts until its `'token limit'` or until logout. The idle timeout `'token interval'` is removed; datastores report every token they hold as active, so it rarely ended a session anyway.
- Deploying with a `tokens.json` that holds sessions, such as one from a publish, no longer fails with "token key must be 63 bytes"; the check now uses the key size the session manager issues.
- Authentication domains: claim cycles, dropped domain clients and connection errors are handled more robustly.
- Builds for darwin-arm64.
- The package ships an agent guide (AGENTS.md).
- An OpenID authority can have a client secret, `'openid authority client secrets'`, keyed like `'openid authority client ids'`. The session manager sends it when it redeems a login code, which Google requires for a "Web application" client and Entra for a "Web" redirect URI.

`config.alan` is unchanged. The configuration of the session manager in a deployment has one new option, `'openid authority client secrets'`: add it to every deployment, as `( )` when no authority has a secret. `'token interval'` is removed: delete it from every deployment.
