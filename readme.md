# GIC Cinema Booking System

## Requirements

- Python 3.11
- requirements.txt
- Tested on Window OS

## Design Principles
1. GIC cinema booking system is build with SOLID principle in mind, keeping the functions small and purposeful.
Each individual function have only one task.
2. This project is also build with both OOP and functional programming in mind. 

### Assumptions
1. The movie title can only be one word.
2. When all of the seats are booked and the user choose option 1, it should immediately reject the option and notify the user that there are no more seats.
3. At the seat selection stage, there are no way back to the main menu.
4. When the user wants a lot of tickets and the user chooses a seat that is very near the screen. If there are not enough seats in the row in front, there will be an alert to notify the user that there are not enough seats to overflow in front.
5. In the updated version, it is assumed that if the user wants a lot of tickets and the user manually choose their seats that are very close to the screen, if there are not enough seats in front row, it will overflow to the most rear row, starting from the middle with the same rule as the default seat arrangement.

## Installation
### Option 1: Clone the repository and change directory into the repository
<details open>

```bash
git clone git@github.com:Chiaope/GIC_Cinema.git
cd GIC_Cinema
```
</details>

### Option 2: Unzip Folder
<details open>

```
Unzip the GIC_Cinema folder and open a terminal in the unzipped folder's path
```
</details>

## Start
### Create python virtual environment, activate it and install all of the required dependencies

```bash
python -m venv "venv_gic_cinema"
venv_gic_cinema\Scripts\activate
pip install -r requirements.txt
```

### Run the python program
```bash
# Normal verion
python GIC_Cinema.py

# Updated manual selected seating arrangement version
python Updated_GIC_Cinema.py
```