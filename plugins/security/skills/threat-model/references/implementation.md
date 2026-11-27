# Security control references

Use [OWASP ASVS](https://asvs.owasp.org/) for testable web/service controls; [MASVS/MASTG](https://mas.owasp.org/MASVS/) for mobile; [Web Top 10](https://top10.owasp.org/2025/0x00_2025-Introduction/) for risk discovery, not a complete verification standard. [NIST SSDF](https://csrc.nist.gov/projects/ssdf) supplies lifecycle responsibilities.

Each control record: versioned requirement, applicability, asset/threat, implementation location, negative test, owner, evidence and expiry/revisit condition. Example: a tenant-scoped download must deny another tenant before generating a bearer URL; separately document any already-issued URL's revocation window.
