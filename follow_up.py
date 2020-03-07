import sqlite3

def display_sales(results):
    print("Select one sales followed for more detailed information")
    for i in range(len(results)):
        print("|" + str(results[i][0]).center(5) + "|")
    selection = input()
    return selection

def select_sales(selection):

