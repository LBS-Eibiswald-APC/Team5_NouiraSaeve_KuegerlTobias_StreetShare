import { test, expect } from '@playwright/test';

test('ST-TOOL-002 filters and pagination work together', async ({ page }) => {
  await page.setViewportSize({ width: 1400, height: 1000 });

  await page.goto('/login');
  await page.locator('[data-test="login-email"]').fill('tkugerl@gmail.com');
  await page.locator('[data-test="login-password"]').fill('tobias123');
  await page.locator('[data-test="login-submit"]').click();

  await expect(page).toHaveURL(/\/main/);

  await expect(page.locator('[data-test="filter-city"]')).toBeVisible();

  await page.locator('[data-test="filter-city"]').fill('Wien');
  await page.locator('[data-test="filter-zip"]').fill('1010');
  await page.locator('[data-test="filter-apply"]').click();

  await expect(page.locator('[data-test="per-page-select"]')).toBeVisible();
  await page.locator('[data-test="per-page-select"]').selectOption('50');

  await expect(page.locator('body')).toContainText(/Seite/i);

  if (await page.locator('[data-test="pagination-next"]').isEnabled()) {
    await page.locator('[data-test="pagination-next"]').click();
    await expect(page.locator('body')).toContainText(/Seite/i);
  }

  await page.locator('[data-test="filter-city"]').fill('Graz');
  await page.locator('[data-test="filter-apply"]').click();

  await expect(page.locator('body')).toContainText(/Seite 1 von|Seite 1/i);
});