# Judge Rubric

Use this rubric before public release.

## Product/Architecture Judge

Evaluate:

- The repo has a clear purpose.
- Scope is narrow and credible.
- Code maps cleanly to the documented architecture.
- README can be understood by a new technical visitor.
- The project does not overclaim autonomy or production maturity.

## Security/Safety Judge

Evaluate:

- No secrets, tokens, private keys, raw logs, private memory, or personal data.
- Live posting/account mutation is not enabled.
- Approval gates are explicit.
- High-risk actions require exact confirmation in future adapters.
- Secret scan and tests pass.

## Launch/UX Judge

Evaluate:

- Launch narrative is strong.
- X drafts are useful and non-spammy.
- Image prompts are clear enough to generate public assets.
- Operator commands are exact.
- Remaining launch blockers are explicit.

Each judge returns:

- PASS or FAIL
- Evidence
- Critical issues
- Required fixes
- Optional improvements
- Confidence score from 1 to 10

