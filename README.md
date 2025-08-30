# api-tcc

## Getting started

This repository contains an academic project developed as part of a TCC (final graduation project).  
It provides a **REST API built with Python (Falcon framework)** that consumes data from **WeatherAPI** and returns weather forecasts in JSON format.  

The API is designed to be simple, well-documented, and reusable for both academic and practical use cases.

---

## Name

**API-TCC** — Weather Forecast API

---

## Description

The API connects to the [WeatherAPI](https://www.weatherapi.com/) service, processes the data, and exposes endpoints with translated and normalized weather information.

### Main Features
- ✅ Real-time weather forecasts (temperature, humidity, pressure, wind, and conditions).  
- ✅ **Translation** of WeatherAPI field names from English to Portuguese.  
- ✅ **Unit conversion** (e.g., Kelvin → Celsius, m/s → km/h).  
- ✅ REST-compliant structure for easy integration.  

This project can be used as:
- A study case for **software engineering** and **API development**.  
- A lightweight backend for apps, dashboards, or IoT systems that require weather data.  

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/VitorTG/api_tcc.git
   cd api_tcc

2. Install dependencies:
   ```bash
pip install -r requirements.txt

2. Configure your WeatherAPI key (via .env or environment variable)::
WEATHER_API_KEY=your_api_key_here


## Support

Issues can be opened directly on the GitHub repository: https://github.com/VitorTG/api_tcc/issues
Contributions and suggestions are welcome!


## Contributing

Create your feature branch
Open a Pull Request: https://github.com/VitorTG/api_tcc/pulls


## Authors and acknowledgment
Developed by VitorTG as part of his graduation project.
Special thanks to open-source libraries, the WeatherAPI, and Python’s developer community.

## License
open-source