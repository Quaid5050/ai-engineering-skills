# Modernization reference

Use differential tests for serializers/parsers and behavior-preserving transformations; use golden data only when reviewed and synthetic. A changed dependency may require updating test infrastructure, but changed production behavior needs explicit acceptance.

Legacy architecture baselines have owner, rationale and shrinking scope. Do not assert an empty baseline when exceptions exist. Static import checks cannot prove semantic domain placement or dynamic loading behavior.
