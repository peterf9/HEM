# HEM — HomeLab Enterprise Monitor

> **Declarative Infrastructure Modeling, Build & Observability Platform for Home Assistant**

[![Python 3.13+](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![Status v1.0 Stabilization](https://img.shields.io/badge/Status-v1.0%20Stabilization-green.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

HEM is a high-performance infrastructure modeling and compilation engine that translates declarative asset definitions into production-ready Home Assistant packages, Lovelace dashboards, inventory records, and telemetry metrics.

---

## 🎯 User Profiles & Quickstart Guides

### 1. 🟢 Beginner User (Asset Integrator)

Get started in 3 simple commands:

```bash
# Initialize a new HEM project with sample assets
hem init

# Compile infrastructure into Home Assistant packages
hem build

# Safely deploy compiled packages to Home Assistant
hem deploy
```

---

### 2. 🟡 Operator (Infrastructure Observability & Diagnostics)

Maintain and inspect environment health:

```bash
# Run system diagnostics and compute Build Health Score (0-100)
hem doctor

# Trace entity provenance (Entity -> Capability -> Provider -> Asset)
hem explain binary_sensor.hem_brume_availability

# Preview change impact before deploying
hem plan

# Generate a visual Mermaid dependency graph
hem graph
```

---

### 3. 🔵 Provider Developer (Extension Author)

Create and publish custom provider plugins:

```bash
# Scaffold a new provider extension package
hem new snmp

# Validate implementation against HEM Provider SDK v1
hem sdk-validate ping

# Auto-generate updated Markdown documentation
hem docgen
```

---

## 🛠️ CLI Reference Matrix

| Command | Purpose / Question Answered |
| --- | --- |
| `hem init` | Initializer: *"How do I set up a new HEM project instantly?"* |
| `hem build` | Build Engine: *"Does my infrastructure definition compile cleanly?"* |
| `hem plan` | Execution Plan: *"What assets, entities, and files will change before deploy?"* |
| `hem deploy` | Deploy Manager: *"How to safely deploy packages to Home Assistant with backup?"* |
| `hem doctor` | Operational Doctor: *"Is my build environment healthy and valid?"* |
| `hem explain` | Provenance Tracer: *"From which asset, provider, and template did this entity originate?"* |
| `hem graph` | Dependency Graph: *"How to visualize my asset-to-entity architecture?"* |
| `hem new` | Scaffold Manager: *"How do I start creating a new provider extension?"* |
| `hem search` | Provider Catalog: *"Is there an official or community provider available?"* |
| `hem providers` | Registry Inspector: *"Which providers are installed and what capabilities do they offer?"* |
| `hem sdk-validate` | SDK Validator: *"Is my custom provider 100% compliant with Provider SDK standards?"* |
| `hem docgen` | Doc Generator: *"How to automatically document my infrastructure in Markdown?"* |

---

## 📄 Platform Governance & Documentation

- **[ARCHITECTURE_DECISIONS.md](ARCHITECTURE_DECISIONS.md)**: Architectural decisions summary and v1.0 readiness checklist.
- **[COMPATIBILITY_POLICY.md](docs/COMPATIBILITY_POLICY.md)**: Semantic versioning policy, Core API freezes, and SDK deprecation guidelines.
- **[DOMAIN_MODEL.md](docs/DOMAIN_MODEL.md)**: Domain contracts for Assets, Sources, and Entities.
- **[PROVIDER_SDK.md](docs/PROVIDER_SDK.md)**: Guidelines for writing custom Providers and Capabilities.

---

## 📜 License

Distributed under the **MIT License**.
