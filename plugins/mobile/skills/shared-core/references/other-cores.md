# Other ways to share a core

The rules of the skill (core decides, shells only wire; no exceptions across the boundary; tested once on both targets; lint for purity) apply to every option.

| Option | Fits when | Notes |
|---|---|---|
| **Kotlin Multiplatform** | Android is native Kotlin already; iOS shell in Swift | See `kmp.md` |
| **Rust core** (UniFFI or `swift-bridge` + JNI) | Heavy computation, crypto, or a core also used on desktop/server | Errors as `Result` mapped to return values, never panics across FFI (`catch_unwind` at the boundary); generate bindings in CI |
| **C++ core** (Djinni-style bindings) | Existing C++ code base | Same rules; no exceptions across the C ABI |
| **Core in the cross-platform framework's language** (Dart in Flutter, TypeScript in React Native) | Background logic can run in the framework's runtime (headless isolate/JS task) | Simplest when the OS lets that runtime run in the background; native shells then only wire OS callbacks to it. Check the background limits first: a killed process may not restart the runtime |
| **Duplicate in each platform language** | Tiny, stable rules only | Then keep a shared set of test vectors (JSON input → expected decision) run by both platforms' tests so they cannot drift |

Whatever is chosen is recorded as a decision (why, what it locks in, when to revisit).
