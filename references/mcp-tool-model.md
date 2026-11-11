# MCP Tool Model
<!-- Factory reference. Read during workflows/02-analyze.md and 05-generate-skill.md. -->

A generated skill never makes raw HTTP calls. It instructs Claude to use an **MCP tool** that
calls the REST API. The skill is written against the **tool contract**, with the REST contract
behind it.

## The boundary (do not cross it)
- A skill that tells Claude how to use an MCP tool is NOT an MCP server implementation.
- The factory reads MCP tool contracts as INPUT. It never generates or modifies MCP servers.
- MCP's job at runtime is only to call REST and return JSON. It does not transform data.

## What to capture from a tool contract
- Tool name and the endpoint(s) it fronts.
- Input arguments: names, types, which are required, and how they map to the endpoint's
  path/query/body/headers.
- Output shape: the JSON the tool returns (used to drive presentation and evals).
- Any auth the tool handles vs. auth the skill must supply.

## Mapping the skill to the tool
For each user task the skill supports, record: which tool to call, with which arguments, in
what order (for multi-step sequences), and how to aggregate multiple responses. Put this in the
skill body or a per-endpoint reference, each line traceable to a source.

## If a needed tool does not exist
Do not invent a tool or fall back to raw HTTP. Record it as an unknown/dependency and ask
(see clarification-bank.md). The skill can only use tools that are actually exposed.
