"""Minimal runnable snippet for the ADR: one key, three observability signals.

errors.capture + flags.set + metrics.report — the lightweight unified stack the
ADR selects. See README.md for the decision and the comparison table. Each call
is a single Infrai REST call (see infrai.py); note the three DISTINCT prefixes.
"""
import infrai


def demo() -> None:
    # 1) Feature flag (replaces a flags vendor)  -> POST /v1/flags/set
    infrai.flags.set(
        key="new_pipeline",
        type="bool",
        default_value=False,
        enabled=True,
        description="Controls the new MVP pipeline rollout.",
    )

    # 2) Metric (replaces a self-built metrics pipeline)  -> POST /v1/metrics/report
    infrai.metrics.report(type="counter", name="pipeline.runs", value=1, tags={"stage": "mvp"})

    # 3) Error capture (replaces an error-tracking vendor)  -> POST /v1/errors/capture
    try:
        raise RuntimeError("example failure")
    except RuntimeError as exc:
        infrai.errors.capture(message=str(exc), level="error", context={"stage": "mvp"})


if __name__ == "__main__":
    demo()
    print("set one flag, reported one metric, captured one error — all with one key")
