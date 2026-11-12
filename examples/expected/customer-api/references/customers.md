# Endpoint contracts: customers
<!-- Loaded on demand. Every line traces to a source. -->

## GET /customers/{id}  (MCP: get_customer)
- Path param: id (integer, required). Source: OpenAPI.
- Auth: Bearer token required. Source: OpenAPI security + best-practices.md. [REQ-AUTH]
- 200 -> Customer { id, name, email, created_at }. Source: OpenAPI schema + example.
- 401 -> missing/invalid token. Source: OpenAPI.
- 404 -> no such customer. Source: OpenAPI.
- 403 -> UNKNOWN (not documented). Ask before handling. [REQ-403]

## POST /customers  (MCP: create_customer)
- Body: name (string, required), vendor_id (string, required). Source: OpenAPI.
- 201 -> created. Source: OpenAPI.
- 400 -> validation error; vendor_id is required. Source: error example. [REQ-CREATE-VENDOR]
