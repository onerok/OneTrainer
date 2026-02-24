# playwright-cli

Use this skill when the user asks to automate a browser from terminal commands using `playwright-cli`.

## Tool identity
- App name: `playwright-cli`
- Purpose: run Playwright MCP-style browser commands from CLI with persistent sessions.
- Verified in this environment:
  - `playwright-cli --help`
  - `playwright-cli --version` 

## Core rules
- Always use named sessions with `-s=<session>` for multi-step tasks.
- Do not run dependent browser commands in parallel.
- Start with `open`, then `goto`, then interaction commands.
- Use `snapshot` before `click`/`fill` to obtain fresh element refs.
- End with `close` for the session.

## Minimal workflow
1. Start session:
   - `playwright-cli -s=work open`
2. Navigate:
   - `playwright-cli -s=work goto https://example.com`
3. Get refs:
   - `playwright-cli -s=work snapshot`
4. Interact:
   - `playwright-cli -s=work click <ref>`
   - `playwright-cli -s=work fill <ref> "value"`
   - `playwright-cli -s=work type "text"`
5. Collect artifacts if needed:
   - `playwright-cli -s=work screenshot`
   - `playwright-cli -s=work pdf`
   - `playwright-cli -s=work network`
6. Close:
   - `playwright-cli -s=work close`

## Commands to use most
- Navigation: `open`, `goto`, `reload`, `go-back`, `go-forward`
- Interaction: `snapshot`, `click`, `dblclick`, `fill`, `type`, `hover`, `select`, `check`, `uncheck`, `press`
- Tabs: `tab-list`, `tab-new`, `tab-select`, `tab-close`
- Debug: `console`, `network`, `run-code`, `eval`, `show`
- Artifacts: `screenshot`, `pdf`, `state-save`, `state-load`

## Session management and recovery
If you hit socket/session issues (e.g. `EADDRINUSE`):
1. `playwright-cli close-all`
2. `playwright-cli kill-all`
3. `playwright-cli list` (expect no browsers)
4. Re-open a fresh named session

## Notes for this repo
- This skill is for terminal browser automation, not Playwright Test.
- If the user asks for Playwright tests/spec files, switch to `npx playwright test ...` workflow instead.
- Keep steps deterministic: snapshot -> act -> snapshot.
