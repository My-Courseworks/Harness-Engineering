# ADR-0007: Use PostgreSQL for the order service

## Status
Accepted (2026-10-26)

## Context
Problem, constraints, and decision drivers
(e.g., need ACID transactions, team knows SQL, budget for managed hosting).

## Considered Options
1. PostgreSQL
2. MongoDB
3. DynamoDB

## Decision
We will use PostgreSQL, because it is the only option that meets the
transactional requirement while matching the team's existing skills.

### Rejected Alternatives
- **MongoDB**: Multi-document transactions are possible but add complexity;
  our order data is highly relational.
- **DynamoDB**: Vendor lock-in and awkward ad-hoc querying for reporting.

## Consequences
- Positive: Strong consistency, mature tooling, familiar to the team.
- Negative: Horizontal write scaling will need sharding or read replicas later.