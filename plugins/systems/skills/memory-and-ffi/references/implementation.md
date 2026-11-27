# Systems and FFI adapters

- C/C++: RAII where available, explicit C ownership contracts, bounds/overflow checks; AddressSanitizer, UndefinedBehaviorSanitizer and ThreadSanitizer where supported. Verify ABI/layout and compiler options across targets.
- Rust: minimize unsafe blocks, document safety preconditions, use ownership/lifetimes and Result; `catch_unwind` catches unwinding panics only. See [Rust documentation](https://doc.rust-lang.org/std/panic/fn.catch_unwind.html). Consider Miri where the supported subset fits.
- Go: cgo pointer/lifetime rules, context cancellation, race detector and allocation profiles; garbage collection does not eliminate native resource ownership.
- Swift/Kotlin native bridges: actor/thread and runtime lifetime constraints, explicit error bridging and cancellation. See [Kotlin native interop](https://kotlinlang.org/docs/native-objc-interop.html).

Sanitizer success is not a proof of absence; fuzz corpora and coverage need retained reproductions. Test x86/ARM and endianness/alignment assumptions relevant to the supported product.
