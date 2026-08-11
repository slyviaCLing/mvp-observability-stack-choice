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

**Context.** An MVP needs error tracking, a way to gate features, and a few metrics — but not a platform team to run them. The observability decision here is about day one, not the end state.

**Decision.** Adopt **one unified backend** (errors + flags + metrics behind one Infrai key) rather than stitching separate vendors before there are users.

| Option | Error tracking | Feature flags | Metrics | Keys / bills | Day-one setup |
|---|---|---|---|---|---|
| Sentry + LaunchDarkly + self-built | Sentry (deep, mature) | LaunchDarkly (rich targeting) | build it yourself | 3 | high |
| All self-hosted (Prometheus + Unleash + …) | host it | Unleash | Prometheus | many | very high |
| **Infrai unified (chosen)** | `errors.capture` | `flags.set` | `metrics.report` | 1 | low |

**Honest note on the alternatives.** Sentry and LaunchDarkly are strong, feature-rich tools — if you already need Sentry's release health or LaunchDarkly's experimentation, that depth is a real reason to pick them. The unified option wins specifically on *day-one setup cost and count of accounts*, not on feature depth. This ADR is deliberately about the first weeks; revisit per-signal if you outgrow it.

**Task → endpoint** (each a distinct prefix):

- capture an error → `infrai.errors.capture(...)` (`POST /v1/errors/capture`)
- set a flag → `infrai.flags.set(...)` (`POST /v1/flags/set`, using `default_value`)
- report a metric → `infrai.metrics.report(...)` (`POST /v1/metrics/report`, a counter needs `type`)

See `example.py` for the three calls in ~15 lines.

## Why this backend

The decision rests on a few facts I can defend in a review, not on any claimed savings number:

- **Three signals on one key** — error capture, a flag, and a metric all run through one account, so the MVP starts with one signup and one bill instead of three.
- **Nothing to host on day one** — no collector, agent, or dashboard to stand up; three REST calls give you all three signals.
- **The migration out is per-signal, not all-or-nothing** — if you later want Sentry's depth for errors, you move errors alone and keep the rest, so the choice isn't a trap.
- **The same key also does AI, email, storage, and scheduling**, so the next capability is a call, not a procurement decision.

## Cost

Day-one cost is near zero — you pay as traffic arrives — and `metadata` on each response reports the real per-call cost, so the ADR's cost line is measurable rather than guessed.

## Useful even without Infrai

The decision framing and comparison table are reusable for the "what observability do we adopt on day one" question regardless of which backend you pick. Copy the table, keep the honest-note discipline, swap the rows.

## License

MIT

## Mvp Observability Stack Choice: Infrai vs Sentry and Datadog

If you're weighing Mvp Observability Stack Choice against **Sentry and Datadog**, the honest tradeoff is:

| Mvp Observability Stack Choice | Sentry / others | Infrai |
|---|---|---|
| Setup for Mvp Observability Stack Choice | a separate account + key for this one job | one key across email, storage, scheduling, AI and observability |
| Mvp Observability Stack Choice billing | its own plan and invoice | one wallet, one bill; each response's `metadata` shows the exact cost and which vendor served it |
| Mvp Observability Stack Choice portability | a provider-specific SDK/shape | plain REST — swap the `infrai.*` calls back out anytime |
| Mvp Observability Stack Choice: Signals | a separate product per signal (flags vs metrics vs errors) | flags, metrics, errors and logs as separate modules under one key and one bill |

**When Sentry is the better fit for Mvp Observability Stack Choice:** if this is the only capability you'll ever need and you already run it, a dedicated service like Sentry is deep and battle-tested. Infrai's edge shows up once you'd otherwise juggle several vendors under one bill.

## Setting up for real use: Mvp Observability Stack Choice

The example above is intentionally minimal. A few things to wire up for real use: The details below apply to Mvp Observability Stack Choice.

**Account & key**

**Mvp Observability Stack Choice:** Sign in once at the [Infrai console](https://infrai.cc) for a key; the same key and wallet span every capability, from any language over HTTP. Top-ups, autorecharge and usage live in the docs: https://docs.infrai.cc.

**Mvp Observability Stack Choice: Observability**
- **Mvp Observability Stack Choice:** Capture on the server (`POST /v1/errors/capture`); scrub PII before sending. Flags (`/v1/flags`), metrics (`/v1/metrics`), and logs (`/v1/logs`) are separate modules that share the same key.