CREATE TABLE roles (
    id INT(11) NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL COLLATE 'utf8mb4_general_ci',
    created_at DATETIME NULL DEFAULT current_timestamp(),
    PRIMARY KEY (id) USING BTREE
);

CREATE TABLE users (
    id INT(11) NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
    last_name VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
    display_name VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
    hashed_pw VARCHAR(255) NOT NULL COLLATE 'utf8mb4_general_ci',
    email VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
    phone VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
    street VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
    house_nr VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
    zip VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
    role_id INT(11) NULL DEFAULT NULL,
    created_at DATETIME NULL DEFAULT current_timestamp(),
    city VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
    country VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
    PRIMARY KEY (id) USING BTREE,
    UNIQUE INDEX email (email) USING BTREE,
    INDEX fk_users_role (role_id) USING BTREE,
    CONSTRAINT fk_users_role FOREIGN KEY (role_id) REFERENCES roles (id) ON UPDATE RESTRICT ON DELETE SET NULL
);


CREATE TABLE tools (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT NULL,
  base_price DECIMAL(10,2),
  deposit DECIMAL(10,2),
  tool_condition VARCHAR(255),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  created_by INT,

  CONSTRAINT fk_tools_creator
    FOREIGN KEY (created_by)
    REFERENCES users(id)
    ON DELETE SET NULL
);


CREATE TABLE transactions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  tool_id INT NOT NULL,
  borrower_id INT NOT NULL,
  lender_id INT NOT NULL,
  start_date DATETIME NOT NULL,
  end_date DATETIME,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT fk_transactions_tool
    FOREIGN KEY (tool_id)
    REFERENCES tools(id)
    ON DELETE CASCADE,

  CONSTRAINT fk_transactions_borrower
    FOREIGN KEY (borrower_id)
    REFERENCES users(id)
    ON DELETE CASCADE,

  CONSTRAINT fk_transactions_lender
    FOREIGN KEY (lender_id)
    REFERENCES users(id)
    ON DELETE CASCADE
);

INSERT INTO roles (id, name) VALUES (1, 'admin'), (2, 'user');