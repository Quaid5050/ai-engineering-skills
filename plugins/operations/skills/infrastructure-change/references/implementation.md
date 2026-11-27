# Infrastructure adapters

- AWS/Azure/GCP: workload identities, account/project/subscription boundaries, IAM policy, network egress, managed encryption and regional availability differ. Use provider-specific references and actual plan output.
- Terraform/OpenTofu-style IaC: lock providers, protect state, serialize changes and preserve a reviewed plan; plan output can contain secrets.
- Kubernetes: non-root containers where feasible, minimal capabilities, read-only root filesystem, resource requests/limits, probes, graceful termination, disruption policy and workload identity. A readiness probe must reflect actual traffic readiness.
- Serverless: concurrency, cold starts, event replay, timeout, payload size and retry semantics.
- Containers: minimal pinned images, dependency inventory, no embedded credentials, explicit architectures and verified startup/shutdown.

Use [SLSA](https://slsa.dev/spec/v1.2/) and [secure CI guidance](https://docs.github.com/en/actions/reference/security/secure-use) for artifact/build boundaries. Provider deployment remains unverified until exercised in the authorized target.
