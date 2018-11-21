# Release notes Yoda version 1.1 (March 2018)

## New features since Yoda version 1.0
- Update metadata of published packages in the vault
- Copying data packages from vault to research area
- Add support for flexible date fields to metadata form
- Add support for geo location fields to metadata form
- Prevent parallel execution of the same background process
- Default data access is set to restricted
- Fix incorrect access rights after folder move
- Fix incorrect pagination in research area
- Fix incorrect creator name in intake module
- Upgrade CodeIgniter to 3.1.7

## Upgrading from 1.0
Upgrade is supported by Ansible (2.5.x). No migrations required.


## Known Issues
- When storage data is available, different tiers are assigned, and all resources are then reset to the same tier, the statistics module may show a blank page
- Ordering of data in tables is not working. Clicking column sort headers have been disabled and are not shown.
