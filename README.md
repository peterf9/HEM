# HEM - HomeLab Enterprise Monitor

> Enterprise-grade observability framework for Home Assistant.

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Alpha-orange.svg)

---

## Overview

HEM (HomeLab Enterprise Monitor) is an observability framework designed for Home Assistant.

Instead of manually creating hundreds of sensors, templates and automations, HEM generates them automatically from declarative asset definitions.

The project is inspired by enterprise monitoring platforms such as:

- Datadog
- Zabbix
- Grafana
- Prometheus
- Azure Monitor

while remaining fully compatible with Home Assistant.

---

## Project Structure

```
HEM/
│
├── hem/
│   ├── cli.py
│   ├── loaders/
│   ├── contracts/
│   ├── validators/
│   ├── generators/
│   ├── runtime/
│   ├── exceptions/
│   ├── templates/
│   └── utils/
│
├── src/
│   ├── assets/
│   ├── providers/
│   ├── dashboards/
│   └── policies/
│
├── output/
├── tests/
├── docs/
├── pyproject.toml
├── README.md
└── LICENSE
```

---

## Current Status

Current version: **Sprint 0 — Foundation**

The project is under active development.

---

## License

MIT
