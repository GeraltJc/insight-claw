# ClawHub Publishing

This note records the verified release path for publishing the Insight Claw Hermes Skill to ClawHub.

## Verified Release

- ClawHub slug: `insight-claw-hermes`
- Display name: `Insight Claw Hermes`
- Verified published version: `insight-claw-hermes@0.3.0`
- Local skill directory: `skills/hermes/insight-claw-hermes`
- Verified publish tool: ClawHub CLI

## Preflight

Run these checks from the repository root:

```bash
git status --short --branch
.venv/bin/python -m pytest tests/test_hermes_skill_contract.py
```

Confirm ClawHub login:

```bash
/Users/jc/.hermes/node/bin/clawhub whoami
```

If login is missing or expired, use device-code login:

```bash
/Users/jc/.hermes/node/bin/clawhub login --device
```

## Publish

Use the ClawHub CLI directly:

```bash
/Users/jc/.hermes/node/bin/clawhub skill publish skills/hermes/insight-claw-hermes \
  --slug insight-claw-hermes \
  --name "Insight Claw Hermes" \
  --version <semver-version> \
  --changelog "<release notes>"
```

Example of the verified 0.3.0 release:

```bash
/Users/jc/.hermes/node/bin/clawhub skill publish skills/hermes/insight-claw-hermes \
  --slug insight-claw-hermes \
  --name "Insight Claw Hermes" \
  --version 0.3.0 \
  --changelog "Publish Hermes-specific Insight Claw skill slug for ClawHub discovery."
```

Do not reuse a published version. Bump the semver version for each new ClawHub release.

## Verify

After publishing, verify the listing:

```bash
/Users/jc/.hermes/node/bin/clawhub search insight-claw-hermes
/Users/jc/.hermes/node/bin/clawhub inspect insight-claw-hermes
```

Expected successful publish output shape:

```text
Published insight-claw-hermes@<version> (<release-id>)
```

Expected inspect fields:

```text
Latest: <version>
Moderation: CLEAN
```

`Moderation Reason: pending.scan` can appear immediately after publishing while ClawHub finishes asynchronous scanning.

## Avoid These Paths

These paths are not the verified direct ClawHub publishing path:

- `hermes skills publish ... --to clawhub`: currently reports that ClawHub publishing is not yet supported.
- `hermes skills publish ... --to github --repo GeraltJc/insight-claw`: creates a GitHub submission PR instead of directly publishing to ClawHub.
- `https://clawhub.ai/submit`: currently returns 404.

## Common Failures

- `clawhub: command not found`: use `/Users/jc/.hermes/node/bin/clawhub` or install the ClawHub CLI.
- Expired login: run `/Users/jc/.hermes/node/bin/clawhub login --device`.
- Version already exists: bump `--version`.
- Network or DNS failure in Codex sandbox: rerun the command with escalated permissions.
- Moderation is not immediately final: inspect the listing again after scan completion.
