# Cryptica_project

## Story
This project started in January 2016 because of a nice puzzle game I fuond in the app store. Since stages were increasingly difficult to solve with minimum moves (thus with highest score) and since the game gives that number when solving a stage, I though it would be nice to model levels (with matrices and numbers to identify objects) and try to solve them using brute force.

## Ideas
To begin with, I started with a python script since I felt better programming in python. Later on, I decided to switch to C++ due to execution time issues.
Main ideas were:
1- represent moves: up (U), down (D), left (L), right (R).
2- generate many strings of moves (e.g. "LLRUURLUDL")
3- try every string generated and wai for the solution.

In this approach there were many problems in terms of inefficiency and performances, which lead me to find many solutions and improvements. They are better described in the documentation.
