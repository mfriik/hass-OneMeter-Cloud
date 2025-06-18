# OneMeter Integration for Home Assistant

This custom integration connects [OneMeter](https://onemeter.com) devices to Home Assistant via their REST API. It fetches energy and battery data, exposes them as sensors, and optionally creates a Utility Meter helper for seamless integration with Home Assistant’s Energy Dashboard.

---

## 🚀 Features

- Retrieves data including:
  - Firmware version
  - Last readout timestamp
  - Battery level (%)
  - Usage level (kWh)
  - This month's and previous month's consumption
- Allows users to:
  - Set a custom device name (support multiple devices)
  - Configure scan interval (in seconds)
- Automatically:
  - Creates a Utility Meter helper entity for monthly energy tracking
  - Enables smooth integration with Home Assistant’s Energy view

---

## 🧰 Installation

1. Copy the `onemeter/` directory into your Home Assistant `custom_components/` folder:  
   `<config_dir>/custom_components/onemeter`
2. Restart Home Assistant.
3. Navigate to **Settings > Devices & Services > Add Integration**, then search for **OneMeter** and follow the setup flow.

---

## ⚙️ Configuration

During setup, you will need to provide:

- **API Key:** Obtain from [cloud.onemeter.com/#/api](https://cloud.onemeter.com/#/api)  
- **Device ID:** Found at [cloud.onemeter.com/#/devices](https://cloud.onemeter.com/#/devices) (click your device and find the device ID in the URL, e.g., `***000a000-0000-0000-0000-000000000000***`)  
- **Device Name:** Used to name entities for easier identification  
- **Scan Interval:** How frequently to poll the API (in seconds)

> ⚠️ The OneMeter API updates roughly every 15 minutes. Polling more frequently may be useful during troubleshooting but could overload their servers. Please use responsibly.

---

## 💡 Utility Meter Integration

The integration automatically creates a Utility Meter helper entity that tracks monthly energy consumption, compatible with Home Assistant’s **Energy Dashboard**.

Example entity:  
`utility_meter.garage_meter_consumption`

Add this entity in:  
**Settings > Dashboards > Energy > Grid Consumption**

---

## 📊 Example Entities

If your device name is `Garage Meter`, entities will be named like:

| Entity ID                                  | Description                       |
|--------------------------------------------|---------------------------------|
| `sensor.garage_meter_firmware_version`     | Firmware version                 |
| `sensor.garage_meter_last_refresh`         | Timestamp of last Home Assistant update |
| `sensor.garage_meter_last_readout`         | Timestamp of OneMeter data readout |
| `sensor.garage_meter_battery_level`        | Battery percentage               |
| `sensor.garage_meter_usage_level`          | Total usage in kWh               |
| `sensor.garage_meter_current_month_consumption` | Current month's energy usage     |
| `sensor.garage_meter_previous_month_consumption` | Previous month's energy usage    |
| `utility_meter.garage_meter_consumption`   | Monthly tracked energy usage helper |

---

## 📜 License

This project is licensed under the MIT License.

---

### Repository

Find the source code and contribute here:  
[https://github.com/mfriik/hass-OneMeter-Cloud](https://github.com/mfriik/hass-OneMeter-Cloud)
