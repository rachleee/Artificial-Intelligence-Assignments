#Rachel Lee
#0695297
#COIS 4550H
#Assignment #2
#March 24, 2024

#Description: The python program is to implement the hill climbing algorithm to solve the 8-queen probllem

import random
import time
import numpy as np
from sklearn.base import BaseEstimator #Using sklearn because that was what the TA recommended to use during class

#printing the chess board
def print_board(board):
        for row in board:
            print(" ".join("Q" if col == row else "_" for col in range(len(board)))) #printing a text chess board where Q is the queen and _ is the rest of the space

#############################################################################################################
#                                                                                                           #
#                #Version 1 will use Random-restart hill climbing                                           #
#                #The program will start at a random state                                                  #
#                #If it reaches a local maxima, restart w/ another random state                             #
#                #Heursitic cost <-- # of attacking/conflicting pairs to measure goodness of the state      #  
#                #Max number of restarts = 100                                                              #
#                                                                                                           #
#############################################################################################################
            

#reference is from: https://scikit-learn.org/stable/modules/generated/sklearn.utils.shuffle.html
#a usefule reference: https://webstersprodigy.net/2009/10/31/8-queens-problem-hill-climbing-python/
#another reference: https://solarianprogrammer.com/2017/11/20/eight-queens-puzzle-python/
            
################################# Version 1: #################################
            

class Part1(BaseEstimator): #using BaseEstimator from sklearn
    def __init__(self, n=8, max_restarts=100): #making max restart for the hill climbing to be 100 with n=8 for the queens
        self.n = n #making n to be the instance variable for self.n
        self.max_restarts = max_restarts #making max_restart to be the instance variable of self.max+restart


    #initial_board method that generates a random chess board
    #reference is: https://www.codeease.net/programming/python/how-to-create-chess-board-numpy
    def initial_board(self):
        return np.array([random.randint(0, self.n-1) for _ in range(self.n)]) 

    #heuristic_cost method that calculates the number of attacking queens on the board (the heuristic cost)
    def heurisitic_cost(self, board):
        conflicts = 0 #initializing conflict to be zero
        for i in range(self.n): #for each queen on the chess board
            for j in range(i+1, self.n): #itierating the remaining queens after the current row
                if board[i] == board[j] or abs(board[i] - board[j]) == j - i: #checks for horizontal or diagonal attacks of the queens
                    conflicts += 1 #increment conflict if there is conflict
        return conflicts

    #hill_climbing method for random start
    #reference to time.time() is: https://www.geeksforgeeks.org/python-time-module/
    def hill_climbing(self):
        start_time = time.time() #recording the start time
        best_board = self.initial_board() #getting the best chess board config for the queens
        best_conflicts = self.heurisitic_cost(best_board) #calculating the attacking conflicts for the best board

        for _ in range(self.max_restarts): #iterating for a max of 100 restarts
            current_board = self.initial_board() #generates a initial_board for the current self 
            current_conflicts = self.heurisitic_cost(current_board) # calculating the attacking conflicts for the current self
            

            while current_conflicts > 0: #while there are sill conflicts

                #print(f"Current state: {current_board}")  #this was to check how the state looked like and how many conflicts there were for the queens
                #print(f"Current conflicts: {current_conflicts}")

                successors = [] #initalizing an empty list
                for col in range(self.n): #for every queen on the board
                    for row in range(self.n):#iterating for the potential postion that a queen may take
                        if current_board[col] != row: #if the queen in the current column is not in the same row
                            successor = current_board.copy() #make a copy of the current board to change and modify it
                            successor[col] = row #make the queen in the row of the column to be in successor
                            successors.append(successor) #adds it to successor

                best_successor = min(successors, key=self.heurisitic_cost) #obtaining best_successor based on the lowest heuristic cost
                best_successor_conflicts = self.heurisitic_cost(best_successor) #calculates the amount of conflicts

                if best_successor_conflicts < current_conflicts: #if the better successor's conflict is less than the current, it will make best_successor to be the new board
                    current_board = best_successor
                    current_conflicts = best_successor_conflicts
                else: 
                    break 

            if current_conflicts < best_conflicts: #if the current_conflict is less than the best_conflicts, it will make cureent to be the new board
                best_board = current_board
                best_conflicts = current_conflicts

        end_time = time.time() #the end time of the execution
        total_time = end_time - start_time

        return best_board, best_conflicts, total_time

#main block to print
if __name__ == "__main__":
    solver = Part1(n=8, max_restarts=100)

    for _ in range(10): #executing the program 10 times
        final_board, final_conflicts, total_time = solver.hill_climbing() #calling the hill_climbing to find the best solution

        initial_board = solver.initial_board()  # printing what the inital board was

        #printing out the inital chess board
        print("Initial chess board:")
        print_board(initial_board)

        #printing out the final chess board
        print("Final chess board:")
        print_board(final_board)
        print(f"Number of attacking pairs: {final_conflicts}")
        print(f"Total time taken: {total_time:.4f} seconds\n")
        print(f"-"*50)



#############################################################################################################
#                                                                                                           #
#                #Version 2 will use First-choice hill climbing with random-restart                         #
#                #The program will generate random states 1 at a time                                       #
#                #If it reaches a bad state, it will be ignored                                             #
#                #Heursitic cost <-- # of attacking/conflicting pairs to measure goodness of the state      #  
#                #Max number of restarts = 100                                                              #
#                                                                                                           #
#############################################################################################################
        


#Note: I used most of the code in version 1, but deleted the self.max_restarts and added the self.max_successors
        


################################# Version 2: #################################                     

class Part2(BaseEstimator): #using BaseEstimator from sklearn
    def __init__(self, n=8, max_successors=100): #making max restart for the hill climbing to be 100 with n=8 for the queens
        self.n = n  #making n to be the instance variable for self.n
        self.max_successors = max_successors #making max_successor to be the instance variable of self.max_successor

    #initial_board method that generates a random chess board
    def initial_board(self):
        return np.array([random.randint(0, self.n-1) for _ in range(self.n)])

    #heuristic_cost method that calculates the number of attacking queens on the board (the heuristic cost)
    def heurisitic_cost(self, board):
        conflicts = 0
        for i in range(self.n):
            for j in range(i+1, self.n):
                if board[i] == board[j] or abs(board[i] - board[j]) == j - i:
                    conflicts += 1
        return conflicts

    #hill_climbing method for random start
    def hill_climbing(self):
        start_time = time.time()
        best_board = self.initial_board()
        best_conflicts = self.heurisitic_cost(self.initial_board())

        for _ in range(self.max_successors): #iterating for a max of 100 restarts
            current_board = self.initial_board() #generates a initial_board for the current self 
            current_conflicts = self.heurisitic_cost(current_board) #calculating the attacking conflicts for the current self

            for _ in range(self.max_successors): #to generate random state one at a time
                random_col = random.randint(0, self.n - 1) #generating a random number to represent a column index
                random_row = random.randint(0, self.n - 1) #generating a random number to represent a row index
                successor = current_board.copy() #copying the original chess board to modify
                successor[random_col] = random_row #updating the copied board by placing a queen in a random row
                successor_conflicts = self.heurisitic_cost(successor) #checks the number of conflicts of the new board 

                if successor_conflicts < current_conflicts:
                    current_board = successor
                    current_conflicts = successor_conflicts
                    if current_conflicts == 0:
                        break  #if it found a solution with 0 conflict, it will stop generating more successors

                if current_conflicts < best_conflicts:
                    best_board = current_board
                    best_conflicts = current_conflicts

        end_time = time.time()
        total_time = end_time - start_time

        return best_board, best_conflicts, total_time

#main block to print
if __name__ == "__main__":
    solver = Part2(n=8, max_successors=100)

    for _ in range(10): #executing the program 10 times
        final_board, final_conflicts, total_time = solver.hill_climbing() #calling the hill_climbing to find the best solution

        initial_board = solver.initial_board()  # printing what the inital board was

        #main block to print
        print("Initial chess board:")
        print_board(initial_board)

        #printing out the final chess board
        print("Final board configuration:")
        print_board(final_board)
        print(f"Number of attacking pairs: {final_conflicts}")
        print(f"Total time taken: {total_time:.4f} seconds\n")
        print(f"-"*50)