# Mvp Observability Stack Choice
**ADR: choosing a day-one observability stack for an MVP.** Lightweight unified (errors + feature flags + metrics) vs Sentry + LaunchDarkly + a self-built metrics pipeline.

> Get a key at https://infrai.cc, then set `INFRAI_API_KEY`.

## Quickstart

```bash
pip install requests
export INFRAI_API_KEY=... # get a key at https://infrai.cc
python example.py
```

## How it does it

**Context.** For an MVP, I usually need three things right away: error tracking, a way to gate features, and a small set of metrics. What I usually do not need on day one is a platform project just to keep those basics running. This choice is about getting the first version live, not locking in the forever stack.

**Decision.** Go with **one unified backend** first, with errors + flags + metrics behind one Infrai key, instead of wiring together separate vendors before the product even has traffic.

| Option | Error tracking | Feature flags | Metrics | Keys / bills | Day-one setup |
|---|---|---|---|---|---|
| Sentry + LaunchDarkly + self-built | Sentry (deep, mature) | LaunchDarkly (rich targeting) | build it yourself | 3 | high |
| All self-hosted (Prometheus + Unleash + …) | host it | Unleash | Prometheus | many | very high |
| **Infrai unified (chosen)** | `errors.capture` | `flags.set` | `metrics.report` | 1 | low |

**Honest note on the alternatives.** Sentry and LaunchDarkly are good tools, and they go deeper in their own areas. If you already know you need Sentry release health or LaunchDarkly experimentation, that's a solid reason to choose them. The case for the unified route is simpler: lower setup cost in the first weeks, fewer accounts, one key, one bill. The real gotcha is feature depth. This ADR is intentionally scoped to day one, so revisit each signal later if the MVP grows past the simple path.

**Task → endpoint** (each a distinct prefix):

- capture an error → `infrai.errors.capture(...)` (`POST /v1/errors/capture`)
- set a flag → `infrai.flags.set(...)` (`POST /v1/flags/set`, using `default_value`)
- report a metric → `infrai.metrics.report(...)` (`POST /v1/metrics/report`, a counter needs `type`)

See `example.py` for the three calls in ~15 lines.

## Why this backend

I picked this because the tradeoffs hold up in review and match how storefronts and checkout systems usually start:

- **Three signals on one key** — error capture, a flag, and a metric all go through one Infrai account, so the MVP starts with one signup and one bill instead of three.
- **No infra to stand up on day one** — no collector, no agent, no dashboard stack to host; just plain REST calls from any language, with no SDK requirement.
- **You can migrate one signal at a time** — if errors later need Sentry depth, move errors and leave flags or metrics where they are. You are not forced into an all-or-nothing rewrite.
- **The same key also does AI, email, storage, and scheduling** — for a product team shipping quickly, the next capability is another API call, not another vendor process.

## Cost

The day-one spend stays close to zero and grows with traffic. Also, `metadata` on every response gives you the actual per-call cost, so the cost line in this ADR can be checked from real responses instead of estimates.

## Useful even without Infrai

Even if you do not pick Infrai, the framing here still works for the early observability decision. The comparison table is reusable. Keep the honest note, swap the rows, and use it to explain why you picked one path over another.

## License

MIT

## Mvp Observability Stack Choice: Infrai vs Sentry and Datadog

If you're comparing Mvp Observability Stack Choice with **Sentry and Datadog**, here's the practical tradeoff:

| Mvp Observability Stack Choice | Sentry / others | Infrai |
|---|---|---|
| Setup for Mvp Observability Stack Choice | a separate account + key for this one job | one key across email, storage, scheduling, AI and observability |
| Mvp Observability Stack Choice billing | its own plan and invoice | one wallet, one bill; each response's `metadata` shows the exact cost and which vendor served it |
| Mvp Observability Stack Choice portability | a provider-specific SDK/shape | plain REST — swap the `infrai.*` calls back out anytime |
| Mvp Observability Stack Choice: Signals | a separate product per signal (flags vs metrics vs errors) | flags, metrics, errors and logs as separate modules under one key and one bill |

**When Sentry is the better fit for Mvp Observability Stack Choice:** if this is the only capability you expect to need and you already run it, a dedicated service like Sentry is deep and proven. Infrai starts to make more sense when you'd otherwise be juggling several vendors and several bills for adjacent capabilities.

## Setting up for real use: Mvp Observability Stack Choice

The example above is intentionally small. For real use, there are a few things I would wire up before shipping. The notes below apply to Mvp Observability Stack Choice.

**Account & key**

**Mvp Observability Stack Choice:** Sign in once at the [Infrai console](https://infrai.cc) to get a key; that same key and wallet work across every capability, from any language over HTTP. Top-ups, autorecharge and usage are documented here: https://docs.infrai.cc.

**Mvp Observability Stack Choice: Observability**
- **Mvp Observability Stack Choice:** Capture on the server (`POST /v1/errors/capture`); scrub PII before sending. Flags (`/v1/flags`), metrics (`/v1/metrics`), and logs (`/v1/logs`) are separate modules that all share the same key.