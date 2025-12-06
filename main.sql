
--Q- A. CREATE TABLE
CREATE TABLE staff_info (
    Emp_no INT PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Rank VARCHAR(20) CHECK (Rank IN ('manager', 'officer', 'accountant')),
    Date_of_join DATE,
    Salary INT CHECK (Salary BETWEEN 6500 AND 20000)
);

--Q- B. INSERT RECORDS
INSERT INTO staff_info (Emp_no, Name, Rank, Date_of_join, Salary)
VALUES
    (101, 'John Smith', 'manager', '2008-01-15', 18000),
    (102, 'Sarah Johnson', 'officer', '2009-03-20', 12000),
    (103, 'Michael Brown', 'accountant', '2007-07-10', 15500),
    (104, 'Emily Davis', 'manager', '2009-11-05', 19500),
    (105, 'David Wilson', 'officer', '2008-02-28', 8000);

-- Q -C. QUERY: Name, Salary, and Tax (12% if salary >= 15000, else 1%)
SELECT Name,Salary,
    CASE
        WHEN Salary >= 15000 THEN Salary * 0.12
        ELSE Salary * 0.01
    END AS Tax
FROM staff_info;

--Q- D. QUERY: Employees joined between 1/1/2007 and 1/1/2010
SELECT * FROM staff_info
WHERE Date_of_join BETWEEN '2007-01-01' AND '2010-01-01';

-- queries extra 
SELECT * FROM staff_info;

SELECT * FROM staff_info WHERE Rank = 'manager';

SELECT Rank, AVG(Salary) AS Average_Salary
FROM staff_info
GROUP BY Rank;

SELECT Name, Salary
FROM staff_info
WHERE Salary > 15000
ORDER BY Salary DESC;
