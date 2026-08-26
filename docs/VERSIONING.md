# Release versioning policy

Codex Access Toolkit versions follow the current stable NVDA release.

- The base add-on release uses the NVDA stable version, such as `2026.1`.
- Add-on-only patches append a third component: `2026.1.1`, `2026.1.2`, and so on.
- Patch numbering increases for every published add-on update while NVDA 2026.1
  remains the current stable NVDA release.
- When a newer stable NVDA version is released, the add-on starts a matching new
  version line. For example, NVDA 2026.2 starts add-on version `2026.2`, followed
  by `2026.2.1`, `2026.2.2`, and so on as patches are published.
- Preview, beta, release-candidate, and development NVDA versions do not start a
  new add-on version line. Only a stable NVDA release does.
- The manifest version, source version constant, build-script default, release
  notes, changelog heading, package filename, and release tag must agree before
  publishing.
- Existing historical versions are not renamed. Version 2026.1.1 was the first
  patch release using this policy.

Before preparing any future release, confirm the latest stable NVDA version and
apply this policy. Do not publish a package whose version follows an outdated
NVDA stable release line.
