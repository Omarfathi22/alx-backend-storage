# MySQL Advanced - Unique Users Table

This project contains SQL scripts for creating a unique users table in MySQL.

## Script

- `0-uniq_users.sql`: Creates a table named `users` with the following attributes:
  - `id`: Integer, never null, auto increment and primary key.
  - `email`: String (255 characters), never null and unique.
  - `name`: String (255 characters).

### Instructions

To run the script, execute the following command in your MySQL environment:

```bash
mysql -uroot -p < path/to/0-uniq_users.sql
