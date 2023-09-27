## Django Cars - Rent
#### You can use the rent a cars project I made according to your wishes.

## Description

The aim of the project is for users to rent a comfortable, luxury and economy
class vehicle and to easily compare and choose the vehicles they will rent.
When users first enter the website, the home page welcomes them. Users can
go to the Automobiller page to look at the vehicles and easily find the vehicle
they want thanks to the filters. The user can add any vehicle he wishes to his wish
list and add it to the comparison list by clicking on the scale icon. There are 2 options
for the vehicle ordered. 1 vehicle is picked up from the office, 2 vehicles are delivered to
the airport by the company employee. I did not make a payment system because the payment will
be paid to the company employee in both ways. Each time a vehicle is ordered, information regarding
order details and a code to cancel the order are sent to the user's e-mail address. Users can view the
questions and answers on the Frequently Asked Questions (FAQ) page. If they want to make any other questions
or requests, they can reach us via Contact Us. There is a job postings page in my project. Users can view active
job postings and apply here. At the time of application, the user can add a CV if he wishes. If the CV is a file
that is not in pdf format, an error message appears on the page for the user. I used Jinja template engine as template
language in the project. I made the backend with Python's Django framework.

## Installation
````bash
git clone https://github.com/elizamin-orucov/car_book_rent_a_cars.git .
pip install -r requirements.txt
django-admin startproject Core .
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
````