# Model integration reference

Use the project's installed provider SDK and current official API documentation; do not invent model names or unsupported parameters. Examples of official references: Anthropic's [Messages API](https://docs.claude.com/en/api/messages); OpenAI's [Responses API](https://platform.openai.com/docs/api-reference/responses) and [evaluation guidance](https://developers.openai.com/blog/eval-skills). Whichever provider the project uses, read its own API reference and review its data-retention terms; each provider needs its own adapter.

A fixture should model: transport timeout; rate limit with retry delay; invalid structured output; refusal; truncated stream; cancellation; valid result; and a provider/model version change. Use a fake provider for deterministic boundary tests and an explicitly authorized held-out live evaluation for model quality. Store request templates and labels without secrets or personal data.

Example acceptance record: task_success=measured fraction with sample size; schema_failures=count; unsafe_actions=count; p95_latency=measured; cost_per_success=measured. Set project thresholds before comparing candidates; no universal score is supplied.
