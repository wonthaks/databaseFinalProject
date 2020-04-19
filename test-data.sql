INSERT INTO Items
  (stockNum, borrowedNum, price, manufacturer, type)
VALUES
  (1, 1, 300, 'Medicines are us', 'Antibiotics'),
  (5, 2, 200, 'Dinomatrics', 'Face mask'),
  (2, 0, 10, 'Dental Measures', 'Tongs');

INSERT INTO Staff
  (name, department, age, address, phoneNum)
VALUES
  ('Joe Smith', 'Human Resources', 38, '2251 Sherman Avenue NW, Washington DC, 20001', '202-883-0455'),
  ('John Cena', 'Security', 40, '2255 E John Street, Sunnyvale CA, 94086', '202-444-9960'),
  ('Mary Lenny', 'Doctor', 37, '1234 N Doc Street, Pittsburgh PA, 12034', '202-465-7889');

INSERT INTO Uses
  (itemID, staffID, dateBorrowed, dateReturned)
VALUES
  (2, 1, '2017-06-02', '2020-02-13'),
  (3, 1, '2019-12-14', '2020-02-01'),
  (2, 2, '2020-02-03', '2020-02-05'),
  (3, 3, '2020-03-14', '2020-04-15'),
  (2, 1, '2020-02-03', '2020-02-13'),
  (2, 2, '2020-03-15', NULL),
  (2, 3, '2019-11-15', NULL),
  (1, 2, '2020-02-15', NULL);
