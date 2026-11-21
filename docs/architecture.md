# Architecture

The bot is a three-stage pipeline:

```
ingest (job_dispatcher, url_resolver)
    -> processors (watch_processor)
        -> infrastructure (browser_factory, report_writer, session_vault)
```

## Stage contracts

- **Ingest** produces `ViewJob` dataclasses.
- **Processor** consumes `ViewJob`, drives the browser, returns `ViewResult`.
- **Infrastructure** abstracts Playwright and disk I/O so the processor
  stays testable with fakes (see `tests/test_watch_processor.py`).

## Concurrency model

`JobDispatcher` yields N jobs; `WatchProcessor.run_batch` gathers them
with `asyncio.gather`. Concurrency is bounded by the number of jobs
emitted, so tune `runtime.concurrency` in `config/settings.yaml`.

## Fingerprint layer

`BrowserFactory` injects a per-context user agent, viewport, and locale
chosen from pools in `config/`. This is the only place that talks to
Playwright directly — everything else stays library-agnostic.