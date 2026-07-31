# HEM Domain Model Specification

> Version 1.0

This document specifies the core domain contracts and models of the **HomeLab Enterprise Monitor (HEM)** framework.

Any breaking changes to these specifications require an **Architecture Decision Record (ADR)**.

---

# Domain Model Hierarchy

```
Asset
  │
  ├── Provider
  │     │
  │     └── Capability
  │
  ├── Source
  │
  └── Inventory
        │
        └── Manifest & Artifacts
```

---

# 1. Asset Contract

An **Asset** represents a monitored infrastructure entity.

```python
class Asset(BaseModel):
    id: str
    name: str
    provider: str
    class_name: str  # JSON/YAML alias: 'class'
    type: Optional[str] = None
    vendor: Optional[str] = None
    model: Optional[str] = None
    firmware: Optional[str] = None
    serial: Optional[str] = None
    location: Optional[str] = None
    owner: Optional[str] = None
    criticality: str = "medium"
    tags: List[str] = []
    description: Optional[str] = None
    source: Source
```

---

# 2. Source Contract

A **Source** defines entity bindings in Home Assistant.

```python
class Source(BaseModel):
    availability: str
    latency: str
    jitter: str
    packet_loss: str
```

---

# 3. Provider & Capability Contracts

A **Provider** declares supported monitoring capabilities (e.g., `availability`, `latency`, `jitter`, `packet_loss`).

```
Provider
   │
   ├── ping
   ├── snmp
   ├── rest
   └── mqtt
```

---

# 4. Inventory & Manifest

The **Inventory** (`inventory.json`) acts as the Single Source of Truth compiled from assets.
The **Manifest** (`manifest.json`) tracks build metadata, execution statistics, and generated entity mappings.

---

# Architectural Guarantee

Core contracts are **frozen** as of Release Candidate 0.1.0-alpha.
