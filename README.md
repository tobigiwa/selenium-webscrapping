# Webscraping and Automation with Selenium

## Project Description

This project demonstrates an elaborate webscraping program that spans mutilple webpages using Selenium with Python.

## Project Objective

Automaing and designing a maintainable codebase for scraping mutiple webpages using Selenium with python.

* A script(soup.py) of a Python Class with it only attribute as the browser driver and **it methods are function doing a singular scraping job**.

* A script(cooking.py) with a context manager variable calling each function and appending the scrape data to a list of dictionaries.

* A script(chopping.py) responsible for managing extra transformation needed for the scrape data.

* A script(create_log.py) to create logging for our code.

## Running the script

Run `pip install -r requirement.txt` in your activated virtualenv to have all needed dependencies.

Run `python cooking.py` to execute the program. The list of dictionaries is converted into a Pandas Dataframe which is then written to tab seperated file format.

The repo also includes another script that houses the codebase in a single script(served.py).

I do hope my code brings good readability. :+1: :+1:
