# HEM Compatibility Policy Specification

> Version 1.0

This document outlines the versioning, stability guarantees, and compatibility policy for the **HomeLab Enterprise Monitor (HEM)** platform.

---

# Versioning Strategy

HEM follows **Semantic Versioning 2.0.0** (`MAJOR.MINOR.PATCH`).

```
  v1 . 0 . 0
  │   │   └── Patch: Backward-compatible bug fixes
  │   └────── Minor: Backward-compatible features & capabilities
  └────────── Major: Breaking architectural changes (requires ADR)
```

---

# 1. Core API Stability

- **Core Contracts & Runtime**: `Asset`, `Source`, `BuildContext`, `ExecutionStatus`, `EventBus`, and `Paths` are **frozen**.
- Any breaking modification to Core contracts requires a formal **Architecture Decision Record (ADR)** approved by maintainers.

---

# 2. Provider SDK Compatibility

- Providers built against **SDK v1** (`BaseProvider`, `ProviderMetadata`, `BaseCapability`) are guaranteed backward compatibility within the `1.x` release series.
- SDK deprecation warnings will be published at least one Minor version prior to removal.

---

# 3. Manifest & Inventory Schema Versioning

- `manifest.json` uses an independent `manifest_version` integer.
- `inventory.json` uses an independent `inventory_version` integer.
- Forward and backward schema migrations are handled cleanly without disrupting existing Home Assistant deployments.

---

# 4. Migration & Deprecation Policy

- **Deprecation Warning**: Features marked for deprecation emit warnings via `hem doctor` and CLI logs.
- **Migration Guides**: Breaking schema changes will include automatic CLI migration tooling (`hem migrate`).
