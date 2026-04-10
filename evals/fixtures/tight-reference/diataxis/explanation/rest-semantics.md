# Why Status Codes Matter

## The 200-for-everything antipattern

Some APIs return 200 for every response and put the real status in the body:

```json
{"status": "error", "code": 404, "message": "Not found"}
```

This breaks every tool built on HTTP semantics. Caches can't tell success from
failure. Load balancers can't detect unhealthy backends. Retry logic can't
distinguish transient errors (503) from permanent ones (404). Monitoring
dashboards show 0% error rate while the application is on fire.

## Status codes enable generic error handling

A well-behaved API lets clients write one error handler per status class:

- **4xx**: the client made a mistake — show the error to the user, don't retry
- **5xx**: the server failed — retry with backoff, alert if persistent
- **2xx**: success — process the response

Without correct status codes, every API needs custom error parsing. With them,
a single HTTP client library handles errors from any API the same way.

## Precision reduces support burden

When a client gets 401, they know to re-authenticate. When they get 403, they
know their credentials are valid but insufficient. When they get 429, they know
to wait. Each code is a specific diagnosis. Returning 400 for everything forces
the client to parse error messages — messages that change without notice,
break on localization, and vary between endpoints.

For the full code list, see the [reference](../reference/codes.md). For how to
implement error handling in Flask, see the [how-to](../howto/error-handling.md).
