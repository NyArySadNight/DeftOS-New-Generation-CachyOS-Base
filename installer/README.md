# DeftOS installer (CachyOS base)

Installer for the CachyOS-based DeftOS, using the same UI and hardware scan as the Arch edition.

Differences from the Arch edition:
- Kernel: `linux-cachyos-bore` (CachyOS kernel with the BORE scheduler), with `linux-lts` as the fallback.
- Packages come from the CachyOS repo, which the live ISO enables.
- The backend is archinstall. Calamares is not used in this edition.

## Files
- `ui/index.html`: installer UI, same flow as the Arch edition.
- `bin/deftos-hwscan`: read-only hardware scan writing `hw.js`.
- `bin/deftinstall-ui`: runs the scan, serves the UI on 127.0.0.1:8765 and opens a browser.
- `bin/deftinstall`: runs archinstall. `--config FILE` uses the JSON saved from the UI.
- `archinstall.json`: default configuration.

## Use on the live ISO
1. `deftinstall-ui`, then review the steps in the browser.
2. Press Copy config and save it as `archinstall.json`.
3. `sudo deftinstall --config archinstall.json`

## Notes
- The DeftOS kernel is not used in this edition. The CachyOS kernel is the default.
- Snapshots need btrfs for root.
