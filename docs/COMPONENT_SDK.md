# HEM Component SDK Specification

> Version 1.0

This specification describes the **Component Composite Pattern** in the HomeLab Enterprise Monitor (HEM) platform.

---

# What is a Component?

A **Component** is a reusable composite block that encapsulates a group of related **Capabilities**.

While a `BaseProvider` integrates with an external source (e.g. SNMP, Docker, Proxmox), **Components** organize logical equipment subsystems such as networking interfaces, storage volumes, and thermal environments.

---

# Architecture Overview

```
                      BaseProvider (SNMP / Docker / Proxmox)
                                      │
              ┌───────────────────────┼───────────────────────┐
              ▼                       ▼                       ▼
      InterfaceComponent      StorageComponent      EnvironmentComponent
              │                       │                       │
       ┌──────┴──────┐         ┌──────┴──────┐         ┌──────┴──────┐
       ▼             ▼         ▼             ▼         ▼             ▼
   Bandwidth      Errors   Capacity      Storage    Temp        Power
```

---

# Component Taxonomy

## 1. Network Components (`InterfaceComponent`)
Aggregates network telemetry:
- `NetworkBandwidthCapability` (`Mbit/s`)
- `NetworkErrorsCapability` (`errors/s`)
- `NetworkUtilizationCapability` (`%`)

## 2. Storage Components (`StorageComponent`)
Aggregates disk space and volume telemetry:
- `StorageCapability` (`%`)
- `CapacityCapability` (`GB` / `TB`)
- `FreeSpaceCapability` (`GB` / `TB`)

## 3. Environment Components (`EnvironmentComponent`)
Aggregates hardware sensors and thermal conditions:
- `TemperatureCapability` (`°C`)
- `PowerCapability` (`W`)
- `FanCapability` (`RPM`)

---

# Best Practices for Provider Developers

1. **Prefer Composition over Inheritance**: Providers should instantiate Components rather than rendering ad-hoc sensors.
2. **Reuse Existing Capabilities**: Before creating a new Capability, consult the standard taxonomy (`Core`, `Resource`, `Network`, `Service`).
3. **Decouple Data Providers from Renderers**: Components only handle capability rendering and entity metadata; they do not invoke external network calls directly.
