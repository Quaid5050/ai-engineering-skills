# Identity adapters

OAuth/OIDC implementations must follow the selected provider's current protocol/security guidance; use authorization code with PKCE where applicable, exact redirect validation and distinct access/ID token purposes. Browser sessions need CSRF policy, Secure/HttpOnly/SameSite choices appropriate to the flow and fixation-resistant rotation. Native apps need system-browser and secure storage patterns, not embedded credential capture.

For service-to-service access, define workload identity, audience and resource permissions. For passkeys/MFA/recovery, model credential enrollment, backup factors, takeover resistance and revocation. Use established libraries and platform APIs; no homemade JWT verification or encryption scheme.

Control baseline: [OWASP ASVS](https://asvs.owasp.org/). Verify provider/API details for the installed version before implementation.
