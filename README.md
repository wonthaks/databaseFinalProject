# Hospital Inventory Management Documentation

This is a project for the class Database Systems and is done by Ana Luisa Mata Sanchez and Wontha Kyaw San. The link to the readme for this project is here.


## About
This project is a tool to manage hospital inventories and analyze them. With this program, it is possible to manage items by adding them, and reducing or increasing their counts.  It is possible to let existing staff members borrow items if available. Furthermore, there are several options given to the user to analyze the current items being used by the staff. 

## Installation
Flask is required to run this program. To install flask:

`pip3 install flask`

## Usage
Run the program using the following:

`virtualenv --python=3.7 env`

`source activate.sh`

`flask run`

After running, the user will now be able to view the employees in the database, as well as the items currently stored in the inventory. The user will also be able to view all the cases where the employees are using the items.

In the page where the user is shown the items, they will be able to add new items to the database. Furthermore, in the report page for each item will be options to increase or decrease the number of that item the hospital inventory has in stock.

The user will be able to view the details of all the items that a staff member has used or is currently using in the staff history page as well which can be accessed from the staff page. 

Users will be able to return items that have been borrowed as well. This can be done either from the items page or the staff history page, or even from the usage page. 

Additionally, users will be able to analyze the usage of items by using one of two options :
View a desired number of items in the inventory that have been used the least.
View a desired number of items in the inventory that have been least recently used.
