# HTTP Status Codes Reference

## 2xx — Success

| Code | Name | Meaning | API usage |
|------|------|---------|-----------|
| 200 | OK | Request succeeded | GET that returns data, PUT/PATCH that returns updated resource |
| 201 | Created | Resource created | POST that creates a new resource; include `Location` header |
| 204 | No Content | Success, no body | DELETE, or PUT/PATCH when the client doesn't need the result |

## 3xx — Redirection

| Code | Name | Meaning | API usage |
|------|------|---------|-----------|
| 301 | Moved Permanently | Resource URL changed forever | Retired endpoints; clients update bookmarks |
| 302 | Found | Temporary redirect | OAuth flows, short-lived redirects |
| 304 | Not Modified | Cached version is current | Conditional GET with `If-None-Match` / `If-Modified-Since` |

## 4xx — Client Errors

| Code | Name | Meaning | API usage |
|------|------|---------|-----------|
| 400 | Bad Request | Malformed syntax | Unparseable JSON, missing required fields |
| 401 | Unauthorized | No valid credentials | Missing or expired auth token |
| 403 | Forbidden | Valid credentials, insufficient permissions | User authenticated but lacks access |
| 404 | Not Found | Resource does not exist | GET/PUT/DELETE on nonexistent ID |
| 409 | Conflict | Request conflicts with current state | Duplicate creation, optimistic locking failure |
| 422 | Unprocessable Entity | Valid syntax, invalid semantics | Field validation errors (email format, range checks) |
| 429 | Too Many Requests | Rate limit exceeded | Include `Retry-After` header |

## 5xx — Server Errors

| Code | Name | Meaning | API usage |
|------|------|---------|-----------|
| 500 | Internal Server Error | Unhandled exception | Catch-all; log the error, return a generic message |
| 502 | Bad Gateway | Upstream service failed | Proxy or gateway got an invalid response |
| 503 | Service Unavailable | Temporarily overloaded or in maintenance | Include `Retry-After` if possible |
| 504 | Gateway Timeout | Upstream service timed out | Proxy waited too long for a response |

For how to return these from Flask, see the [error handling how-to](../howto/error-handling.md).
For why correct status codes matter, see the [explanation](../explanation/rest-semantics.md).
