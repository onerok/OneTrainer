#!/usr/bin/env bash
set -euo pipefail

SESSION="${PLAYWRIGHT_SMOKE_SESSION:-web-smoke-$RANDOM-$RANDOM}"
WEB_UI_URL="${WEB_UI_URL:-http://127.0.0.1:5173}"
SMOKE_VALUE="playwright-smoke-$(date +%s)"

cleanup() {
  playwright-cli -s="$SESSION" close >/dev/null 2>&1 || true
}
trap cleanup EXIT

playwright-cli -s="$SESSION" open
playwright-cli -s="$SESSION" goto "$WEB_UI_URL"

playwright-cli -s="$SESSION" run-code "async (page) => {
  await page.waitForSelector('main.page-shell');
  await page.waitForSelector('input[name=\"workspace_dir\"]');
}"

playwright-cli -s="$SESSION" run-code "async (page) => {
  await page.locator('input[name=\"workspace_dir\"]').fill('$SMOKE_VALUE');
  await page.getByRole('button', { name: 'Save General Settings' }).click();
  await page.getByText('General settings saved.').waitFor({ state: 'visible' });
}"

playwright-cli -s="$SESSION" run-code "async (page) => {
  await page.reload();
  await page.waitForSelector('input[name=\"workspace_dir\"]');
  const saved = await page.locator('input[name=\"workspace_dir\"]').inputValue();
  if (saved !== '$SMOKE_VALUE') {
    throw new Error('Persistence check failed: expected $SMOKE_VALUE, got ' + saved);
  }
}"

echo "Playwright smoke passed. workspace_dir persisted as: $SMOKE_VALUE"
