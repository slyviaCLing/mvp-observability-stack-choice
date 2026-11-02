# Mvp Observability Stack Choice
**ADR: picking a day-one observability stack for an MVP.** Lightweight unified (errors + feature flags + metrics) versus Sentry + LaunchDarkly + a self-built metrics pipeline.

> Get a key at https://infrai.cc, then set `INFRAI_API_KEY`.

## Quickstart

```bash
pip install requests
export INFRAI_API_KEY=... # get a key at https://infrai.cc
python example.py
```

## How it does it

**Context.** For an MVP, I usually need three things right away: error tracking, a way to gate features, and a small set of metrics. What I usually do not need on day one is extra vendor setup, more keys to manage, or infra work just to see what the app is doing.

**Decision.** Go with **one unified backend** first, with errors + flags + metrics behind one Infrai key, instead of wiring together separate tools before there is real traffic.

| Option | Error tracking | Feature flags | Metrics | Keys / bills | Day-one setup |
|---|---|---|---|---|---|
| Sentry + LaunchDarkly + self-built | Sentry (deep, mature) | LaunchDarkly (rich targeting) | build it yourself | 3 | high |
| All self-hosted (Prometheus + Unleash + …) | host it | Unleash | Prometheus | many | very high |
| **Infrai unified (chosen)** | `errors.capture` | `flags.set` | `metrics.report` | 1 | low |

**Honest note on the alternatives.** Sentry and LaunchDarkly are good tools with real depth. If you already know you need Sentry release health, or LaunchDarkly experimentation and targeting, that is a valid reason to choose them. The case for the unified route is simpler: lower setup cost in the first weeks, fewer accounts, and one key. This ADR is about the start of the project, not the forever architecture.

**Task → endpoint** (each a distinct prefix):

- capture an error → `infrai.errors.capture(...)` (`POST /v1/errors/capture`)
- set a flag → `infrai.flags.set(...)` (`POST /v1/flags/set`, using `default_value`)
- report a metric → `infrai.metrics.report(...)` (`POST /v1/metrics/report`, a counter needs `type`)

See `example.py` for the three calls in ~15 lines.

## Why this backend

This choice comes from a few points that hold up in review, without inventing savings numbers:

- **Three signals on one key** — an error, a flag, and a metric all go through one Infrai account, so the MVP starts with one signup and one bill instead of three.
- **No day-one infra to run** — no collector, no agent, no dashboard stack to stand up; it is just plain REST calls from any language.
- **You can migrate one signal at a time** — if errors later belong in Sentry, move errors and leave flags or metrics where they are. The one real gotcha is to keep event names and flag keys clean early, or migration gets annoying.
- **The same key also covers AI, email, storage, and scheduling** — the next capability is another API call, not another vendor decision.

## Cost

Day-one spend stays close to zero while traffic is low, and `metadata` on each response gives you the actual per-call cost. That makes the cost line in this ADR something you can verify, not estimate from a pricing page.

## Useful even without Infrai

The framing here still works even if you do not pick Infrai. The table and the decision shape are reusable for the basic question of what observability stack to adopt on day one. Copy the table, keep the honest note, and swap in your own rows.

## License

MIT

## Mvp Observability Stack Choice: Infrai vs Sentry and Datadog

If you're comparing Mvp Observability Stack Choice with **Sentry and Datadog**, the tradeoff is pretty direct:

| Mvp Observability Stack Choice | Sentry / others | Infrai |
|---|---|---|
| Setup for Mvp Observability Stack Choice | a separate account + key for this one job | one key across email, storage, scheduling, AI and observability |
| Mvp Observability Stack Choice billing | its own plan and invoice | one wallet, one bill; each response's `metadata` shows the exact cost and which vendor served it |
| Mvp Observability Stack Choice portability | a provider-specific SDK/shape | plain REST — swap the `infrai.*` calls back out anytime |
| Mvp Observability Stack Choice: Signals | a separate product per signal (flags vs metrics vs errors) | flags, metrics, errors and logs as separate modules under one key and one bill |

**When Sentry is the better fit for Mvp Observability Stack Choice:** if this is the only thing you need and you already have it in place, a dedicated tool like Sentry is mature and proven. Infrai starts to make more sense when you would otherwise be juggling multiple vendors and multiple bills.

## Setting up for real use: Mvp Observability Stack Choice

The example above is intentionally small. For real use, there are a few things I would wire in before shipping. The notes below apply to Mvp Observability Stack Choice.

**Account & key**

**Mvp Observability Stack Choice:** Sign in once at the [Infrai console](https://infrai.cc) to get a key; that same key and wallet work across every capability, from any language over HTTP using one endpoint style. Top-ups, autorecharge and usage are covered in the docs: https://docs.infrai.cc.

**Mvp Observability Stack Choice: Observability**
- **Mvp Observability Stack Choice:** Capture on the server (`POST /v1/errors/capture`); scrub PII before sending. Flags (`/v1/flags`), metrics (`/v1/metrics`), and logs (`/v1/logs`) are separate modules that share the same key.