# Static catalogs: TypeScript

## The table: a record keyed by the id union

`satisfies Record<Id, Info>` makes the compiler reject a missing or extra row while keeping literal types.

```ts
export const PLAN_IDS = ["free", "pro", "team"] as const;   // persisted: append only
export type PlanId = (typeof PLAN_IDS)[number];

export interface PlanInfo {
  title: string;
  icon: string;
  monthlyPrice: number;
  seats: number | null;
  group: "personal" | "business";
}

/** Adding a plan: one id above and one row here. */
export const PLANS = {
  free: { title: "Free", icon: "leaf", monthlyPrice: 0, seats: 1, group: "personal" },
  pro:  { title: "Pro", icon: "star", monthlyPrice: 9, seats: 1, group: "personal" },
  team: { title: "Team", icon: "users", monthlyPrice: 29, seats: null, group: "business" },
} as const satisfies Record<PlanId, PlanInfo>;

export const plansIn = (group: PlanInfo["group"]) =>
  PLAN_IDS.filter((id) => PLANS[id].group === group);
```

Avoid `enum` plus a separate `switch` per attribute; avoid a `Record<string, …>`, which loses the exhaustiveness
check.

## Tests

- Pin every row with a frozen expected object (not `PLANS` compared with itself).
- Pin `PLAN_IDS` against a frozen list.
- A schema test (`zod` or the project's validator) when the same data is also loaded at run time.

## When generation is right, the standard tools

| Source of truth | Tool |
|---|---|
| HTTP API schema | `openapi-typescript` / the project's OpenAPI generator |
| A data file shared with another app | A small script in the repo's build, output committed, CI diff check |
| Translations | The project's i18n library's own extraction and typing |
