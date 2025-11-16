# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Changelog save functionality - users can now save update logs to a file
- Timestamp in changelog files for better tracking

### Changed
- Updated package display now shows all packages in one line instead of multiple lines
- Improved changelog formatting with date and time

## [1.0.0] - 2025-11-15

### Added
- Initial release
- Cross-platform update manager
- Support for apt, zypper, dnf, pacman, and brew
- Automatic OS and package manager detection
- Update changelog display showing updated packages
- User confirmation before installing updates
- ASCII banner with project branding

### Features
- Parse package manager output to extract updated packages
- Display count of updated packages
- Professional terminal output with emojis

[Unreleased]: https://github.com/retoro-sen/offdroid_update_manager/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/retoro-sen/offdroid_update_manager/releases/tag/v1.0.0
