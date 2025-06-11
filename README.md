# Home Assistant Person Localtime

A custom integration for Home Assistant that tracks a person's **local time**, **sun position**, **sunrise**, and **sunset times** based on their current location.

Created and maintained by **Rico Eisenstein**.

---

## 🌟 Features

- 🕒 Shows the **person's local time** based on geolocation.
- 🌄 Displays if the **sun is currently above or below the horizon**.
- 🌅 Provides **sunrise and sunset times** adjusted to the person’s local time zone.
- 🔁 Automatically updates every 30 seconds.
- 🧩 Fully set up via the Home Assistant **UI integration flow**.
- 🌐 Supports **multiple languages** (English, Danish, Brazilian Portuguese).

---

## 🧰 Installation

### Option A: Manual Installation

1. Copy the folder `person_localtime/` into: /config/custom_components/
2. Restart Home Assistant.
3. Go to: Settings > Devices & Services > Add Integration
4. Search for **Person Localtime**, then select the `person` entity you want to track.

---

### Option B: HACS Installation (Recommended)

1. In Home Assistant, go to: HACS > Integrations > Custom Repositories
2. Add this URL as a new repository: https://github.com/ricobach/ha_person_localtime select **Integration**.
3. Install **Person Localtime** from the HACS list.
4. Restart Home Assistant and configure via the **UI**.

---

## 🛠 Developer Info

- 🧠 Powered by `DataUpdateCoordinator`
- 📚 Uses [`astral`](https://astral.readthedocs.io), `timezonefinder`, and `pytz`
- 🛠 Fully supports `config_flow` and translations
- 🗂 Follows Home Assistant 2025.6+ architecture guidelines

---

## 🌍 Translations

This integration supports:

- English (`en`)
- Danish (`da`)
- Brazilian Portuguese (`pt-BR`)

Want to help translate? Submit a PR in the `translations/` folder!

---

## 💬 Support

For questions, bugs, or feature requests:

- Open an [issue](https://github.com/ricobach/ha_person_localtime/issues)
- Or contact [@ricobach](https://github.com/ricobach)

---

## 📄 License

This project is licensed under the [Apache License 2.0](LICENSE).

You are free to use, modify, and distribute this software in accordance with the terms of that license.
