# Performance and reliability reference

Open-arrival load models reveal overload differently from closed-loop virtual users; select the model intentionally and account for coordinated omission. Local built-site/lab tests are useful controlled measurements, while real-user and production-equivalent measurements answer different questions.

Backend: query plans, pools, allocations, locks and dependency latency. Web: navigation/rendering, LCP/INP/CLS, payloads and critical resources; do not lazy-load the critical LCP image by default. Mobile: release/profile builds, thermal state, battery baseline and physical devices. Systems: contention, cache behavior and allocations.

Choose a load/profiling tool compatible with the protocol/runtime and required workload; verify its current official documentation and pin the fixture version. A benchmark must retain configuration and dataset shape, not only a screenshot of a number.
