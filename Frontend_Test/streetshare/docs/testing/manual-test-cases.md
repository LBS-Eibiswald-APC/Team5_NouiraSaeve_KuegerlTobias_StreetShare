# StreetShare Manual Test Cases

## AP1 - Frontend Login
- MT-LOGIN-001: Placeholder `max@email.com` is visible on the login page.
- MT-LOGIN-002: Password input masks all entered characters.
- MT-LOGIN-003: `Jetzt registrieren` navigates to `/register`.
- MT-IT-LOGIN-001: Valid credentials log the user in and show the main navigation.
- MT-IT-LOGIN-002: Logout returns the user to `/login`.
- MT-ST-LOGIN-001: Invalid credentials show an error and no redirect happens.
- MT-ST-LOGIN-002: Register validation works for empty, invalid and valid inputs.

## AP2 - Frontend Werkzeug
- MT-TOOL-001: `Neues Tool` modal opens and closes correctly.
- MT-TOOL-002: Tool condition dropdown can be changed.
- MT-TOOL-003: Save button stays disabled until all required fields are filled.
- MT-IT-TOOL-001: Filters work against the real backend.
- MT-IT-TOOL-002: A new tool can be created and shows in the dashboard list.
- MT-IT-TOOL-003: Own tools are visible in `Meine Einträge`.
- MT-ST-TOOL-001: Tool details modal shows all expected fields.
- MT-ST-TOOL-002: Tool form validation and error handling work.
- MT-ST-TOOL-003: Main layout is responsive on desktop, tablet and mobile.
- MT-ST-TOOL-004: Navigation between dashboard and main page stays consistent.
