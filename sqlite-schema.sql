CREATE TABLE IF NOT EXISTS Items (
  itemID INTEGER PRIMARY KEY AUTOINCREMENT,
  stockNum INTEGER,
  borrowedNum INTEGER,
  price INTEGER,
  manufacturer TEXT,
  type TEXT
);

CREATE TABLE IF NOT EXISTS Staff (
  staffID INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  department TEXT,
  address TEXT,
  phoneNum TEXT,
  age INTEGER
);

CREATE TABLE IF NOT EXISTS Uses (
  staffID INTEGER NOT NULL,
  itemID INTEGER NOT NULL,
  dateBorrowed DATE NOT NULL,
  dateReturned DATE,
  PRIMARY KEY(staffID, itemID, dateBorrowed)
);
