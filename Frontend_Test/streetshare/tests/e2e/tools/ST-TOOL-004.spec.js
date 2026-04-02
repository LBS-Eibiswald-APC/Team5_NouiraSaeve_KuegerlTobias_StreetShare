import { test, expect } from '@playwright/test';

test('ST-TOOL-004 dashboard tabs render correctly', async ({ page }) => {
  await page.setViewportSize({ width: 1400, height: 1000 });

  await page.goto('/login');
  await page.locator('[data-test="login-email"]').fill('tkugerl@gmail.com');
  await page.locator('[data-test="login-password"]').fill('tobias123');
  await page.locator('[data-test="login-submit"]').click();

  await expect(page).toHaveURL(/\/main/);

  await page.goto('/dashboard');

  await expect(page.locator('h2').filter({ hasText: 'Dashboard' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Meine Einträge' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Meine Anfragen' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Gesendete Anfragen' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Einstellungen' })).toBeVisible();

  await page.getByRole('button', { name: 'Meine Anfragen' }).click();
  await expect(page.locator('body')).toContainText(/Anfragen/i);

  await page.getByRole('button', { name: 'Gesendete Anfragen' }).click();
  await expect(page.locator('body')).toContainText(/Gesendete Anfragen|Anfragen/i);

  await page.getByRole('button', { name: 'Einstellungen' }).click();
  await expect(page.locator('body')).toContainText(/Einstellungen/i);

  await page.getByRole('button', { name: 'Meine Einträge' }).click();
  await expect(page.locator('[data-test="open-tool-modal"]')).toBeVisible();
});