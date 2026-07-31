# HEM Architecture

> HomeLab Enterprise Monitor
>
> Architecture Specification v1.0

---

# Philosophy

HEM is **not** a Home Assistant package.

HEM is a framework capable of generating Home Assistant configurations from declarative infrastructure definitions.

The Home Assistant YAML files are **artifacts**, never the source code.

---

# High Level Architecture

```
                User Project
                     │
                     ▼
              src/assets/*.yaml
                     │
                     ▼
                Asset Loaders
                     │
                     ▼
               Domain Contracts
                     │
                     ▼
                Validators
                     │
                     ▼
                 Builders
                     │
                     ▼
               File Generators
                     │
                     ▼
        output/packages/hem/*.yaml
                     │
                     ▼
              Home Assistant
```

---

# Project Structure

```
HEM/

├── hem/                # Framework
│
│   ├── builders/
│   ├── contracts/
│   ├── exceptions/
│   ├── generators/
│   ├── loaders/
│   ├── models/
│   ├── runtime/
│   ├── templates/
│   ├── utils/
│   └── validators/
│
├── src/                # User project
│
│   ├── assets/
│   ├── providers/
│   ├── dashboards/
│   └── policies/
│
├── output/             # Generated artifacts
│
├── docs/
│
└── tests/
```

---

# Design Principles

## 1. Assets are the source of truth

Everything starts from Assets.

Nothing else is manually created.

Example:

```
Asset

↓

Provider

↓

Registry

↓

Device

↓

Core

↓

Dashboard
```

---

## 2. YAML is generated

Developers never edit generated YAML.

Generated files may be overwritten at any build.

---

## 3. Framework vs Project

Framework:

```
hem/
```

Project:

```
src/
```

The framework must never depend on project files directly.

---

## 4. Contracts

All communication between modules must happen through Contracts.

Never through dictionaries.

Never through YAML.

Never through JSON.

```
Loader

↓

Contract

↓

Validator

↓

Generator
```

---

## 5. Loaders

Loaders are responsible for reading external data.

Examples:

- YAML
- JSON
- REST API
- Database

Only loaders know where data comes from.

---

## 6. Validators

Validators never read files.

Validators receive fully loaded Contracts.

Their responsibility is only validation.

---

## 7. Builders

Builders coordinate the entire generation process.

Builders do not generate files.

Builders call Generators.

---

## 8. Generators

Generators create output artifacts.

Examples:

- templates.yaml
- groups.yaml
- automations.yaml
- scripts.yaml
- dashboards

One Generator = One responsibility.

---

## 9. Templates

Templates contain presentation logic only.

Business rules must never exist inside Jinja templates.

---

## 10. Runtime

Runtime contains execution context.

Examples:

- configuration
- paths
- cache
- logging
- environment
- version

---

## 11. Exceptions

Every public error must have its own exception class.

Example:

```
AssetValidationError

ProviderNotFound

GeneratorError

BuildError
```

Never raise generic Exception.

---

# Dependency Rules

Allowed:

```
CLI

↓

Builder

↓

Loader

↓

Contract

↓

Validator

↓

Generator
```

Forbidden:

```
Generator

↓

Loader
```

Forbidden:

```
Generator

↓

YAML Reader
```

Forbidden:

```
Validator

↓

Filesystem
```

---

# Build Pipeline

```
src/

↓

Load

↓

Contracts

↓

Validate

↓

Build

↓

Generate

↓

output/

↓

Deploy

↓

Home Assistant
```

---

# Source of Truth

Only these folders contain manually written code:

```
hem/

src/

tests/

docs/
```

Everything inside:

```
output/
```

is disposable.

---

# Code Guidelines

- One class per file whenever practical.
- One responsibility per module.
- Prefer composition over inheritance.
- Prefer immutable models.
- Use Pydantic for all domain models.
- Keep generators stateless.
- Never hardcode filesystem paths.
- Use pathlib everywhere.

---

# Future Roadmap

Framework evolution:

- CLI
- Build System
- Dashboard Generator
- Documentation Generator
- HACS Generator
- Python Integration
- Plugin System

---

# Architectural Rule

If a new feature violates this document,

**the architecture must be discussed before the code is written.**

Architecture is considered part of the product.

---

# Version

Architecture Specification

Version 1.0
