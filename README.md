# OneMeter Integration for Home Assistant

This custom component integrates [OneMeter](https://onemeter.com) devices with Home Assistant via their REST API. It fetches energy and battery data and exposes it as sensors, and optionally creates a Utility Meter helper for use in the Energy Dashboard.

## 🚀 Features

- Retrieves:
  - Firmware version
  - Last readout timestamp
  - Battery level (%)
  - Usage level (kWh)
  - This and previous month's consumption
- Lets users:
  - Set custom device name (for multiple device support)
  - Set scan interval (in seconds)
- Automatically:
  - Adds a Utility Meter helper entity for Energy Dashboard
  - Enables simple integration with Home Assistant's Energy view

## 🧰 Installation

1. Copy the `onemeter/` directory to your Home Assistant `custom_components/` directory: `<config_dir>/custom_components/onemeter`

2. Restart Home Assistant.

3. Go to **Settings > Devices & Services > Add Integration**, then search for **OneMeter**.

## ⚙️ Configuration

During the setup flow, you'll need to provide:

- **API Key** from [cloud.onemeter.com/#/api](https://cloud.onemeter.com/#/api)
- **Device ID** from  [cloud.onemeter.com/#/devices](https://cloud.onemeter.com/#/devices) (Click your device and the device ID will be in the url eg https://cloud.onemeter.com/#/device/***000a000-0000-0000-0000-000000000000*** )
- **Device Name** (used in entity names)
- **Scan Interval** (how often to poll the API in seconds)

> ⚠️ The OneMeter API updates data approximately every 15 minutes. Using a scan interval shorter than that can help during troubleshooting but may unnecessarily burden their servers. Please use responsibly.

## 💡 Utility Meter Integration

The integration creates a Utility Meter helper entity that tracks energy usage per month. This is fully compatible with the Home Assistant **Energy Dashboard**.

- Example: `utility_meter.garage_meter_consumption`

You can find this entity in the **Helpers** list and add it to:
- **Settings > Dashboards > Energy > Grid Consumption**

## 📊 Example Entities

Assuming the device is named `Garage Meter`, you will get:

| Entity ID | Description |
|-----------|-------------|
| `sensor.garage_meter_firmware_version` | Firmware version |
| `sensor.garage_meter_last_refresh` | Timestamp of last update |
| `sensor.garage_meter_last_readout` | Timestamp of OneMeter data |
| `sensor.garage_meter_battery_level` | Battery percentage |
| `sensor.garage_meter_usage_level` | Total usage in kWh |
| `sensor.garage_meter_current_month_consumption` | This month's usage |
| `sensor.garage_meter_previous_month_consumption` | Last month's usage |
| `utility_meter.garage_meter_consumption` | Tracks monthly kWh use |

---

## 📜 License

MIT License.


