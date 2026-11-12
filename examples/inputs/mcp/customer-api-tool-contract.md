# MCP tool contract: customer_api_tool

The skill uses this tool; it is NOT generated or modified by the factory.

| operation | args | fronts | returns |
|---|---|---|---|
| get_customer | id (integer) | GET /customers/{id} | Customer JSON |
| create_customer | name (string), vendor_id (string) | POST /customers | created Customer or 400 error |

Auth: the tool handles the Bearer token; the skill must still instruct that auth is required.
