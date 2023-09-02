# Home Assistant Steam Profile

A custom component (integration) that shows Steam Profile and Lobby information.
This component uses the config flow and can easily be configured via the Integrations section in the UI.

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE.md)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)

![Project Maintenance][maintenance-shield]
[![GitHub Activity][commits-shield]][commits]

## Pre-Installation

Obtain a [Steam Web API Key](https://steamcommunity.com/dev)

## Installation

### HACS Installation

Settings Sync is available in [HACS](https://hacs.xyz) (Home Assistant Community Store).

1. Install HACS if you don't have it already
2. Open HACS in Home Assistant
3. Go to "Integration" section
4. Click 3 dots on top right and custom repository
5. Add `https://github.com/ajagnanan/steam-profile` with catagory `Integration`
6. Search for "Steam Profile" and install
7. In the home assistant configuration screen click on `Integrations`
8. Click on the `+` icon to add a new integration
9. Search for `Steam Profile` and select it
10. Enter your Steam `API Key` and `Account ID` and click `Submit`

### Manual Installation

1. Download the [latest release](https://github.com/ajagnanan/steam-profile/releases).
2. Extract the files and move the `steam_profile` folder into the path to your
   `custom_components`. e.g. `/config/custom_components`
3. In the home assistant configuration screen click on `Integrations`
4. Click on the `+` icon to add a new integration
5. Search for `Steam Profile` and select it
6. Enter your Steam `API Key` and `Account ID` and click `Submit`

[commits-shield]: https://img.shields.io/github/commit-activity/y/ajagnanan/steam-profile.svg?style=for-the-badge
[commits]: https://github.com/ajagnanan/steam-profile/commits/master
[license-shield]: https://img.shields.io/github/license/ajagnanan/steam-profile.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-ajagnanan-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/ajagnanan/steam-profile.svg?style=for-the-badge
[releases]: https://github.com/ajagnanan/steam-profile/releases
