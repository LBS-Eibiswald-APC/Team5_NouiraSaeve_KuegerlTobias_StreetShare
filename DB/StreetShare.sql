CREATE DATABASE IF NOT EXISTS `streetshare`
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE `streetshare`;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `transaction_reviews`;
DROP TABLE IF EXISTS `messages`;
DROP TABLE IF EXISTS `conversations`;
DROP TABLE IF EXISTS `transactions`;
DROP TABLE IF EXISTS `requests`;
DROP TABLE IF EXISTS `tools`;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `roles`;

SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE `roles` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_roles_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) DEFAULT NULL,
  `last_name` VARCHAR(255) DEFAULT NULL,
  `display_name` VARCHAR(255) DEFAULT NULL,
  `hashed_pw` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) DEFAULT NULL,
  `phone` VARCHAR(255) DEFAULT NULL,
  `street` VARCHAR(255) DEFAULT NULL,
  `house_nr` VARCHAR(50) DEFAULT NULL,
  `city` VARCHAR(50) DEFAULT NULL,
  `country` VARCHAR(50) DEFAULT NULL,
  `zip` VARCHAR(50) DEFAULT NULL,
  `role_id` INT DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_users_email` (`email`),
  UNIQUE KEY `uk_users_display_name` (`display_name`),
  KEY `idx_users_role_id` (`role_id`),
  CONSTRAINT `fk_users_role`
    FOREIGN KEY (`role_id`)
    REFERENCES `roles` (`id`)
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `tools` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `description` VARCHAR(500) NOT NULL,
  `base_price` DECIMAL(10,2) DEFAULT NULL,
  `deposit` DECIMAL(10,2) DEFAULT NULL,
  `tool_condition` VARCHAR(255) DEFAULT NULL,
  `tool_image` MEDIUMBLOB NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` INT DEFAULT NULL,
  `deleted` INT NOT NULL DEFAULT 0,
  `deleted_at` DATETIME DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_tools_created_by` (`created_by`),
  CONSTRAINT `fk_tools_creator`
    FOREIGN KEY (`created_by`)
    REFERENCES `users` (`id`)
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `requests` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `tool_id` INT DEFAULT NULL,
  `borrower_id` INT DEFAULT NULL,
  `to_respond_id` INT DEFAULT NULL,
  `lender_id` INT DEFAULT NULL,
  `start_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `end_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `message` TEXT NOT NULL,
  `status` VARCHAR(50) NOT NULL DEFAULT 'Ausstehend',
  PRIMARY KEY (`id`),
  KEY `idx_requests_tool_id` (`tool_id`),
  KEY `idx_requests_borrower_id` (`borrower_id`),
  KEY `idx_requests_to_respond_id` (`to_respond_id`),
  KEY `idx_requests_lender_id` (`lender_id`),
  CONSTRAINT `fk_requests_tool`
    FOREIGN KEY (`tool_id`)
    REFERENCES `tools` (`id`)
    ON DELETE SET NULL,
  CONSTRAINT `fk_requests_borrower`
    FOREIGN KEY (`borrower_id`)
    REFERENCES `users` (`id`)
    ON DELETE SET NULL,
  CONSTRAINT `fk_requests_to_respond`
    FOREIGN KEY (`to_respond_id`)
    REFERENCES `users` (`id`)
    ON DELETE SET NULL,
  CONSTRAINT `fk_requests_lender`
    FOREIGN KEY (`lender_id`)
    REFERENCES `users` (`id`)
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `conversations` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user1_id` INT DEFAULT NULL,
  `user2_id` INT DEFAULT NULL,
  `tool_id` INT DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_conversations_user1_id` (`user1_id`),
  KEY `idx_conversations_user2_id` (`user2_id`),
  KEY `idx_conversations_tool_id` (`tool_id`),
  CONSTRAINT `fk_conversations_user1`
    FOREIGN KEY (`user1_id`)
    REFERENCES `users` (`id`)
    ON DELETE SET NULL,
  CONSTRAINT `fk_conversations_user2`
    FOREIGN KEY (`user2_id`)
    REFERENCES `users` (`id`)
    ON DELETE SET NULL,
  CONSTRAINT `fk_conversations_tool`
    FOREIGN KEY (`tool_id`)
    REFERENCES `tools` (`id`)
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `messages` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `conversations_id` INT DEFAULT NULL,
  `sender_id` INT DEFAULT NULL,
  `content` TEXT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_read` TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `idx_messages_conversations_id` (`conversations_id`),
  KEY `idx_messages_sender_id` (`sender_id`),
  CONSTRAINT `fk_messages_conversation`
    FOREIGN KEY (`conversations_id`)
    REFERENCES `conversations` (`id`)
    ON DELETE SET NULL,
  CONSTRAINT `fk_messages_sender`
    FOREIGN KEY (`sender_id`)
    REFERENCES `users` (`id`)
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `transactions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `tool_id` INT DEFAULT NULL,
  `request_id` INT DEFAULT NULL,
  `borrower_id` INT DEFAULT NULL,
  `lender_id` INT DEFAULT NULL,
  `start_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `end_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `picture_before` MEDIUMBLOB DEFAULT NULL,
  `picture_after` MEDIUMBLOB DEFAULT NULL,
  `status` VARCHAR(50) NOT NULL DEFAULT 'Bezahlt',
  `lender_return_condition` VARCHAR(100) DEFAULT NULL,
  `borrower_return_condition` VARCHAR(100) DEFAULT NULL,
  `final_condition` VARCHAR(100) DEFAULT NULL,
  `return_requested_at` DATETIME DEFAULT NULL,
  `return_confirmed_at` DATETIME DEFAULT NULL,
  `platform_fee` DECIMAL(10,2) DEFAULT NULL,
  `lender_payout` DECIMAL(10,2) DEFAULT NULL,
  `borrower_refund` DECIMAL(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_transactions_request_id` (`request_id`),
  KEY `idx_transactions_tool_id` (`tool_id`),
  KEY `idx_transactions_borrower_id` (`borrower_id`),
  KEY `idx_transactions_lender_id` (`lender_id`),
  CONSTRAINT `fk_transactions_tool`
    FOREIGN KEY (`tool_id`)
    REFERENCES `tools` (`id`)
    ON DELETE SET NULL,
  CONSTRAINT `fk_transactions_request`
    FOREIGN KEY (`request_id`)
    REFERENCES `requests` (`id`)
    ON DELETE SET NULL,
  CONSTRAINT `fk_transactions_borrower`
    FOREIGN KEY (`borrower_id`)
    REFERENCES `users` (`id`)
    ON DELETE SET NULL,
  CONSTRAINT `fk_transactions_lender`
    FOREIGN KEY (`lender_id`)
    REFERENCES `users` (`id`)
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `transaction_reviews` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `transaction_id` INT NOT NULL,
  `borrower_id` INT DEFAULT NULL,
  `lender_id` INT DEFAULT NULL,
  `borrower_condition` VARCHAR(100) DEFAULT NULL,
  `lender_condition` VARCHAR(100) DEFAULT NULL,
  `lender_picture` MEDIUMBLOB DEFAULT NULL,
  `review_status` VARCHAR(50) NOT NULL DEFAULT 'Offen',
  `support_decision_condition` VARCHAR(100) DEFAULT NULL,
  `support_note` TEXT DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `resolved_at` DATETIME DEFAULT NULL,
  `resolved_by` INT DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_transaction_reviews_transaction_id` (`transaction_id`),
  KEY `idx_transaction_reviews_borrower_id` (`borrower_id`),
  KEY `idx_transaction_reviews_lender_id` (`lender_id`),
  KEY `idx_transaction_reviews_resolved_by` (`resolved_by`),
  CONSTRAINT `fk_transaction_reviews_transaction`
    FOREIGN KEY (`transaction_id`)
    REFERENCES `transactions` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `fk_transaction_reviews_borrower`
    FOREIGN KEY (`borrower_id`)
    REFERENCES `users` (`id`)
    ON DELETE SET NULL,
  CONSTRAINT `fk_transaction_reviews_lender`
    FOREIGN KEY (`lender_id`)
    REFERENCES `users` (`id`)
    ON DELETE SET NULL,
  CONSTRAINT `fk_transaction_reviews_resolved_by`
    FOREIGN KEY (`resolved_by`)
    REFERENCES `users` (`id`)
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `roles` (`id`, `name`) VALUES
  (1, 'Admin'),
  (2, 'User');

-- Default admin credentials match docker-compose.yml:
-- email: admin@streetshare.at
-- display_name: admin
-- password: admin123
INSERT INTO `users` (
  `id`,
  `first_name`,
  `last_name`,
  `display_name`,
  `hashed_pw`,
  `email`,
  `phone`,
  `street`,
  `house_nr`,
  `city`,
  `country`,
  `zip`,
  `role_id`
) VALUES (
  1,
  'StreetShare',
  'Admin',
  'admin',
  '$2b$12$piiNNwLsWCKt8K4stqd/ResDRBBo/GoYMFJHUIYUjwYwZDs9Yj9rK',
  'admin@streetshare.at',
  '+4366011111111',
  'Adminhausen',
  '1',
  'Admin',
  'Österreich',
  '8000',
  1
);
