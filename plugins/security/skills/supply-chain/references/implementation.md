# Supply-chain implementation reference

[GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use) covers untrusted workflow input and token boundaries. [SLSA](https://slsa.dev/spec/v1.2/) defines provenance/integrity tracks. [NIST SSDF](https://csrc.nist.gov/projects/ssdf) maps secure development responsibilities.

Choose scanners by coverage: secret detection for credential patterns/history; dependency analysis for vulnerable packages; static analysis for code flows; container/IaC analysis for deployable configuration. Review false positives and avoid several tools that duplicate the same evidence. An SBOM is an inventory, not a vulnerability verdict.

Release acceptance: reviewed source revision, verified dependencies, passing required checks, artifact digest, provenance and restricted signing/publish authorization. Do not claim attestations exist until the actual build/release path produced them.
