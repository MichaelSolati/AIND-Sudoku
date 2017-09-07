# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Firs we accept that the two values in each naked twins pair MUST exist within those boxes. Since constraint propagation is a form of inference, we can determine that the values shared by the naked twins can not possibly exist in any of their peer boxes, so we will filter them out; essentially enforcing constraints on the peer boxes we could not have concluded without the naked twins strategy.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The diagonal sudoku introduces two new `units` to our `unitlist` (going from A1 -> I9, and I1 -> A9). From there it follows the two constraint strategies from lesson #04 (`eliminate` and `only_choice` as well as `naked_twins`, which is better explained above). The `eliminate` strategy allows us to iterate through the board and filter out the single values of a box from the values of that boxes peer: we're able infer that the value in a box of a single value can not exist in the values of a box we are unsure of.

For our `only_choice` strategy what we look to do is we look at the peers of a box and see if it holds a value that none of it's peers holds. If that is the case we can make the assumption that that value must be the actual value of that box.

And we apply these two strategies indefinitely, applying constraints to our board and boxes until we remove all values that do not make sense.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

