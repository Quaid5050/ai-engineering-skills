---
name: ml-lifecycle
description: "Build or revise reproducible model training and serving pipelines. Use for dataset splits, experiments, model evaluation, deployment or drift; not for every LLM API integration."
license: MIT
metadata:
  version: "1.0.0"
---

# Ml Lifecycle

Deliver the requested artifact in `$ARGUMENTS`; do not create infrastructure, accounts or unrelated migrations merely because this procedure mentions them.

## 0. Read the project

Reuse `work-context` and `safe-agent-execution` (foundation plugin). Read the current implementation, actual commands, supported versions and constraints. Load only the applicable parts of [the reference](references/implementation.md). Treat unavailable platform execution as unverified.

## 1. Define the prediction and evidence contract

Specify intended use, forbidden use, label definition, error costs, cohorts and deployment constraints. Establish a simple baseline and an evaluation plan before model selection. Assess data provenance, consent/licensing, leakage and representativeness.

## 2. Build reproducible experiments

Version data snapshots, preprocessing, feature definitions, code, environment, seeds and model artifacts. Split by the actual generalization boundary: time, user, group or site where needed. Fit preprocessing only on training data. Keep the held-out test set out of tuning; report uncertainty and cohort performance, not just one aggregate metric.

## 3. Validate and serve

Test feature parity, missing/out-of-range inputs, numerical stability, calibration and resource usage. Serialization/loading is a code-execution boundary: accept trusted signed/versioned artifacts, not arbitrary pickle-like payloads. Use shadow/canary comparison where appropriate, explicit rollback and compatible feature schemas.

## 4. Monitor and retrain deliberately

Track input/label drift, delayed ground truth, quality by cohort, latency/resource cost and business outcomes. Drift alone does not prove degradation or justify automatic retraining. Gate a replacement through the same held-out/operational checks and record provenance.

## Verification and report

Verify split isolation, preprocessing fit scope, reproducible artifact identity, baseline comparison, schema/feature parity, corrupt/untrusted artifact rejection, rollback and drift alert behavior. Live model quality needs the real authorized dataset.

Report the artifact, decisions, commands/results, revision, environment and remaining uncertainty. Documentation or a local model is not evidence of production or device behavior.

## Rules

- Never claim fairness, robustness or production readiness from one score.
- Keep sensitive training data out of logs and public fixtures.
- Separate experimental success from an approved deployment.

## Composition

| From | This skill | To |
|---|---|---|
| An applicable engineering task | Scoped implementation and acceptance evidence | Relevant tests, security review and deployment readiness; external actions only when authorized |
