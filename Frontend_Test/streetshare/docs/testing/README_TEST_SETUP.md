# StreetShare Test Setup

## Install dependencies
```bash
npm install
npx playwright install
```

## Run unit tests
```bash
npm run test:unit
```

## Run integration tests
```bash
npm run test:integration
```

## Run all Vitest tests
```bash
npm run test
```

## Run E2E tests
```bash
npm run test:e2e
```

## Notes
- Vitest uses `tests/setup.js`.
- Playwright uses `playwright.config.js`.
- Important selectors were added as `data-test` attributes in the app.
