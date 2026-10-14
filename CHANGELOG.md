# Changelog

Earlier releases are listed on the
[GitHub releases page](https://github.com/Xquik-dev/hermes-tweet/releases).

## 0.1.16

- Verified on Hermes Agent v0.22.0. The plugin installs, enables and loads its
  3 tools, 2 commands and the bundled Skill there, as it does on v0.21.7.
- The README links the other Xquik tools by name. PyPI shows the new README
  with this release.
- No behavior changes from 0.1.15.

## 0.1.15

- The README, the docs and both copies of the bundled Hermes Skill read
  without colons or semicolons in their sentences. PyPI shows the new README
  with this release.
- No behavior changes from 0.1.14.

## 0.1.14

- Fix enabling on Hermes Agent v0.21.7. Hermes installed the plugin but left it
  disabled. Hermes resolved the plugin's development dependencies against its
  own pins and found a conflict. The plugin now declares
  `python_runtime: external`, so Hermes installs nothing for it. Enabling failed
  on Hermes Agent v0.21.7. The fix is verified on the same version.
- Remove the README step that installed the PyPI package into Hermes. Current
  Hermes installs have no such environment path.
