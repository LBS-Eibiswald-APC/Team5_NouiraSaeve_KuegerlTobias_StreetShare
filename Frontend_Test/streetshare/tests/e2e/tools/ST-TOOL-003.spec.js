import { test, expect } from '@playwright/test';

test('ST-TOOL-003 deposit is consistent between dashboard and main modal', async ({ page }) => {
  await page.setViewportSize({ width: 1400, height: 1000 });

  await page.goto('/login');
  await page.locator('[data-test="login-email"]').fill('tkugerl@gmail.com');
  await page.locator('[data-test="login-password"]').fill('tobias123');
  await page.locator('[data-test="login-submit"]').click();

  await expect(page).toHaveURL(/\/main/);

  await page.goto('/dashboard');
  await page.evaluate(() => localStorage.setItem('activeTab', 'entries'));
  await page.reload();

  const uniqueName = `DepositTool_${Date.now()}`;

  await expect(page.locator('[data-test="open-tool-modal"]')).toBeVisible();
  await page.locator('[data-test="open-tool-modal"]').click();

  await page.locator('[data-test="tool-name"]').fill(uniqueName);
  await page.locator('[data-test="tool-description"]').fill('Deposit consistency test');
  await page.locator('[data-test="tool-price"]').fill('150');
  await page.locator('[data-test="tool-condition"]').selectOption('Minimal abgenutzt');
  await page.locator('[data-test="tool-image"]').setInputFiles('tests/fixtures/tool.png');

  const dashboardDepositRaw = await page.locator('[data-test="tool-deposit"]').inputValue();

  const dashboardDepositFormatted = new Intl.NumberFormat('de-DE', {
    style: 'currency',
    currency: 'EUR',
  }).format(Number(dashboardDepositRaw));

  await page.locator('[data-test="tool-submit"]').click();
  await expect(page.locator('[data-test="tool-submit"]')).toBeHidden({ timeout: 10000 });

  await expect.poll(async () => {
    return (await page.locator('body').textContent()) || '';
  }, { timeout: 10000 }).toContain(uniqueName);

  await page.goto('/main');
  await page.locator('[data-test="search-name"]').fill(uniqueName);
  await page.locator('[data-test="search-submit"]').click();

  await expect.poll(async () => {
    return (await page.locator('body').textContent()) || '';
  }, { timeout: 10000 }).toContain(uniqueName);

  await page.getByText(uniqueName, { exact: true }).first().click();

  await expect(page.getByText('Tool Details')).toBeVisible();
  await expect(page.locator('body')).toContainText(dashboardDepositFormatted);
});