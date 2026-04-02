-- Optional: vorhandene Tool-Daten leeren, bevor du den CSV/Bild-Import startest.
-- Nur ausfuehren, wenn du die Tool-Tabelle bewusst neu befuellen willst.

SET FOREIGN_KEY_CHECKS = 0;

DELETE FROM messages
WHERE conversations_id IN (
  SELECT id FROM conversations WHERE tool_id IS NOT NULL
);

DELETE FROM conversations
WHERE tool_id IS NOT NULL;

DELETE FROM transaction_reviews
WHERE transaction_id IN (
  SELECT id FROM transactions WHERE tool_id IS NOT NULL
);

DELETE FROM transactions
WHERE tool_id IS NOT NULL;

DELETE FROM requests
WHERE tool_id IS NOT NULL;

DELETE FROM tools;
ALTER TABLE tools AUTO_INCREMENT = 1;

SET FOREIGN_KEY_CHECKS = 1;
