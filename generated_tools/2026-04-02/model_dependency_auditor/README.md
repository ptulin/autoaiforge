# Model Dependency Auditor

## Description

Model Dependency Auditor is a CLI tool that audits Python-based AI projects for vulnerabilities in third-party dependencies. It cross-references dependency versions with known CVEs (Common Vulnerabilities and Exposures) and suggests security updates, ensuring a secure AI development environment.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python model_dependency_auditor.py --file requirements.txt
```

## Features

- Scans `requirements.txt` or `Pipfile` for third-party dependencies
- Checks for known vulnerabilities using public CVE databases
- Suggests secure dependency versions