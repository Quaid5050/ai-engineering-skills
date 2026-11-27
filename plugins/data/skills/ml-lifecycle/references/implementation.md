# ML implementation reference

Use the selected ecosystem's official versioned documentation (for example scikit-learn, PyTorch, TensorFlow or JAX). Distinguish deterministic CPU fixtures from nondeterministic accelerator execution. Record hardware, numeric precision and nondeterministic kernels when relevant.

Example failure fixture: multiple rows per customer must stay within one split; preprocessing fitted on all rows leaks test information. Include temporal leakage, label leakage, imbalanced cohorts and production feature skew. Never select the final model by repeatedly inspecting the held-out test result.

Use [NIST SSDF and its AI community profile](https://csrc.nist.gov/projects/ssdf) for secure lifecycle responsibilities. This does not certify model safety or regulated suitability.
