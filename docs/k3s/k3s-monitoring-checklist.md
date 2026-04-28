## Disclaimer

This checklist is based on environment-specific configurations (hardcoded values such as IP addresses and hostnames).

it is intended for personal documentation and learning purposes only, and may not be directly applicable to other environments without modification.

For a generalized and reproducible setup, refer to the corresponding template-based documentation.

- [x] Check helm version
- [x] If helm is not present, install it and cehck version again
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm version
```
- [x] Added Repo with Prometheus helm
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

