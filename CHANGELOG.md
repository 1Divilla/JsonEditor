# Changelog

## [0.1.6] - 2025-01-28
### Added
- Added functionality to `show_content_file` to display information in the `current_table`.
- Added `data_file` field to `config.json`.
- Renamed `shortcuts` to `binds` for better clarity.
- Renamed variable `app` to `self` for better clarity and consistency.
- Moved `on_right_paned_resize` and `on_principal_resize` to `tools.py`.

### Fixed
- Added handlers for `<<TreeviewOpen>>` and `<<TreeviewClose>>` events to prevent selection during node expansion or collapse.
- The `<<TreeviewSelect>>` event now only triggers `show_content_file` when a node is actually selected, not during expansion or collapse.

### Refactored
- Refactored `open_file` to use `update_treeview` and `insert_items` functions from `tools.py` for better code organization and separation of concerns.

## [0.1.5] - 2025-01-17
### Added
- Implemented `Reset View` functionality.
- Renamed `Toggle Treeview` to `Toggle Table` for better clarity.
- Implemented `Toggle Table` functionality (non-visual).

---

## [0.1.4] - 2025-01-16
### Added
- Added methods to store user-defined proportions of the panels.
- Implemented `Open File` functionality to load and display JSON file contents in the Treeview.

---

## [0.1.3] - 2025-01-15
### Added
- Updated the `Reset Zoom` function:
  - Renamed to `Reset View` to better reflect its expanded functionality.
  - Now resets all visual aspects, including font size and layout proportions, instead of only the font size.
- Added `Save As` function for saving files in JSON format.

---

## [0.1.2] - 2025-01-14
### Added
- Added functions to write and read config file
- Added function to toggle fullscreen
- Added function `Zoom in`, `Zoom out`, `Reset Zoom`

---

## [0.1.1] - 2025-01-13
### Added
- Added shortcuts (currently without functionality).
- Added functionality shortcut(Close: "Ctrl+Q").
- Added functionality for reading files (JSON).
- Minor resizing of elements.

---

## [0.1.0] - 2025-01-10
### Added
- Initial release of the SaveData Editor app.
- Added a menu bar with "File", "Edit", "View", and "Help" options (currently without functionality).
- Implemented basic layout structure with a PanedWindow, file view (treeview), and two tables (still without functionality).

---
