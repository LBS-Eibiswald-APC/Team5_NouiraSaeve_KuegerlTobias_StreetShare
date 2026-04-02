import { test, expect } from '@playwright/test';

test('ST-TOOL-001 create a tool and show it in the main feed', async ({ page }) => {
  await page.setViewportSize({ width: 1400, height: 1000 });

  await page.goto('/login');
  await page.locator('[data-test="login-email"]').fill('tkugerl@gmail.com');
  await page.locator('[data-test="login-password"]').fill('tobias123');
  await page.locator('[data-test="login-submit"]').click();

  await expect(page).toHaveURL(/\/main/);

  await page.goto('/dashboard');
  await page.evaluate(() => localStorage.setItem('activeTab', 'entries'));
  await page.reload();

  await expect(page.locator('[data-test="open-tool-modal"]')).toBeVisible();
  await page.locator('[data-test="open-tool-modal"]').click();

  const uniqueName = `TestTool_${Date.now()}`;

  await page.locator('[data-test="tool-name"]').fill(uniqueName);
  await page.locator('[data-test="tool-description"]').fill('E2E Test Tool');
  await page.locator('[data-test="tool-price"]').fill('150');
  await page.locator('[data-test="tool-condition"]').selectOption('Neu');
  await page.locator('[data-test="tool-image"]').setInputFiles('tests/fixtures/tool.png');

  await expect(page.locator('[data-test="tool-submit"]')).toBeEnabled();
  await page.locator('[data-test="tool-submit"]').click();

  await expect(page.locator('[data-test="tool-submit"]')).toBeHidden({ timeout: 10000 });

  await expect.poll(async () => {
    return await page.locator('body').textContent();
  }, { timeout: 10000 }).toContain(uniqueName);

  await page.goto('/main');
  await page.locator('[data-test="search-name"]').fill(uniqueName);
  await page.locator('[data-test="search-submit"]').click();

  await expect.poll(async () => {
    return await page.locator('body').textContent();
  }, { timeout: 10000 }).toContain(uniqueName);
});