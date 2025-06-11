# Home Assistant Custom Integrations by Rico Eisenstein

This repository contains custom integrations for Home Assistant developed or maintained by Rico Eisenstein. These are placed under the `custom_components/` directory and can be used by copying or linking them into your Home Assistant configuration.

## 📦 Integrations

### [`person_localtime`](custom_components/person_localtime)

Tracks the **local time and sun position** for any Home Assistant `person` entity based on their geolocation.

#### Features:
- Calculates the person's local time based on latitude/longitude.
- Displays sun position (above/below horizon) based on current geolocation.
- Shows sunrise and sunset times in their local time zone.
- Updates every 30 seconds.
- Fully configurable via the Home Assistant UI.

#### Setup:
1. Copy or symlink the `person_localtime` folder to your Home Assistant's `custom_components/`.
2. Restart Home Assistant.
3. Go to **Settings > Devices & Services > Integrations > Add Integration**.
4. Search for **Person Localtime** and select a person.

## 💬 Support

For questions or feedback, open an issue or contact [@ricobach](https://github.com/ricobach).

## 📃 License

MIT License. See [`LICENSE`](LICENSE) for details.
