import { test, expect } from '@playwright/test';

test('ST-LOGIN-002 register a new user and log in again', async ({ page }) => {
  const unique = Date.now();
  await page.goto('/register');

  await page.getByTestId('register-firstname').fill('Test');
  await page.getByTestId('register-lastname').fill('User');
  await page.getByTestId('register-displayname').fill(`Tester${unique}`);
  await page.getByTestId('register-phone').fill('+436641234567');
  await page.getByTestId('register-street').fill('Hauptstraße');
  await page.getByTestId('register-house').fill('1');
  await page.getByTestId('register-zip').fill('1010');
  await page.getByTestId('register-city').fill('Wien');
  await page.getByTestId('register-country').selectOption('Österreich');
  await page.getByTestId('register-email').fill(`test${unique}@example.com`);
  await page.getByTestId('register-password').fill('password123');
  await page.getByTestId('register-confirm-password').fill('password123');
  await page.getByTestId('register-submit').click();

  await expect(page).toHaveURL(/\/login/);
});
