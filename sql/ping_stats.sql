CREATE TABLE ping_stats (
  id INTEGER  UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT,
  outage_time DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL,
  site_id INT
);