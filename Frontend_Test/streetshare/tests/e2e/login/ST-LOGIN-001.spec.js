import { test, expect } from '@playwright/test';

test('ST-LOGIN-001 login -> main -> logout -> login', async ({ page }) => {
  await page.goto('/login');
  await page.locator('[data-test="login-email"]').fill('tkugerl@gmail.com');
  await page.locator('[data-test="login-password"]').fill('tobias123');
  await page.locator('[data-test="login-submit"]').click();

  await expect(page).toHaveURL(/\/main/);
  await page.getByTestId('nav-logout').click();
  await expect(page).toHaveURL(/\/login/);
});
