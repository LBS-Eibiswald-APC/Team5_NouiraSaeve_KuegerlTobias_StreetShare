CREATE TABLE roles (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(255),
  last_name VARCHAR(255),
  display_name VARCHAR(255),
  hashed_pw VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE,
  phone VARCHAR(255),
  address VARCHAR(255),
  house_nr VARCHAR(50),
  zip INT,
  role_id INT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT fk_users_role
    FOREIGN KEY (role_id)
    REFERENCES roles(id)
    ON DELETE SET NULL
);

CREATE TABLE tools (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
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