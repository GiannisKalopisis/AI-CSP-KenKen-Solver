# AI-CSP-KenKen-Solver
A solver for CSP Kenken problem.

## Data Modeling
Kenken puzzle data is modeled in the file as follows:

  - At the forefront is the dimension of the puzzle
  - Each subsequent line of the file represents a puzzle scale and all the features of the puzzle click clauses separated by the character "|"
    - the first part indicates the number that the scale must output
    - the second part indicates the action to be taken on its numbers click
    - all other pieces (eg 0,0 | 1,0 | 1,1) indicate the squares of the puzzle of which the scale is composed

## Puzzle Modeling
The Kenken puzzle is modeled as follows:

  - As **variables** I have set every puzzle box and its scale as well. That is the list of variables is as follows: [(0,0), (0,1), (0,2), (1,0), ..., 0, 1, 2, ...], where 0, 1, 2, ... is the click id.
  - As a domain I have set for variables that are points a list of all possible values, and for the variables that are clustered I have set as a domain a list of tuples, that each tuple has within the possible values that the elements of the click can get. For tuple values, in the case of a variable click, its operation has been calculated that is, there are only prices that satisfy the practice.
  - As a **clique** I set it to be a dictionary that has the click id coming out as a key from the order in which it is read from the file, and as a value has a list, which the first element is the result of the action on the elements of the clique, the second is the action on the elements of the clique and the third is a list of its elements
click.
  - As **neighbors** in the case of simple points I have set the points to be the same line and the same column but also the scale to which it belongs, and in its case clicker I have put the clicker data as neighbors.
  - **clique_number** is a dictionary that has a key as a point e.g. (0.0) and the like value is the id of the click to which it belongs.
  - **inside_same_clique** is also a dictionary where the key is a point e.g. (0.0) and has the value of the rest of its clicks as a value.
  
  
The last two are auxiliary structures and are not necessary for modeling the Kenken puzzle.

The above modeling with the existence of a click as a variable, its values as a tuple in the domain and as a neighbor is to help us convert the constraints to **Binary Constraints**.


## Algorithms
The algorithms used are **BT, BT+MRV, FC, FC+MRV, MAC**. As we will see below some algorithms worked better than others, while some didn't even finish in a reasonable amount of time
 
## Experimental Results
  
  - **Time**:
  
    |                | BT            | BT+MRV     | FC          | FC+MRV       | MAC          |
    | :-------------:|:-------------:|:----------:|:-----------:|:------------:|:------------:|
    |   **3x3**      | 0.00042       | 0.00404    | 0.00041     | 0.00148      | 0.00186      |
    |   **4x4**      | 0.01359       | 0.20588    | 0.00173     | 0.00471      | 0.00485      |
    |   **5x5**      | 39.28007      | 36.94944   | 0.00325     | 0.00814      | 0.01429      |
    |   **6x6**      | -             | -          | 0.02389     | 0.00955      | 0.01555      |
    |   **7x7**      | -             | -          | 2.99562     | 0.18410      | 1.60579      |
    
  - **Assignments**:
  
    |                | BT            | BT+MRV     | FC          | FC+MRV       | MAC          |
    | :-------------:|:-------------:|:----------:|:-----------:|:------------:|:------------:|
    |   **3x3**      | 15            | 91         | 15          | 34           | 13           |
    |   **4x4**      | 319           | 2646       | 46          | 55           | 24           |
    |   **5x5**      | 602840        | 330679     | 78          | 40           | 39           |
    |   **6x6**      | -             | -          | 429         | 88           | 55           |
    |   **7x7**      | -             | -          | 53279       | 1773         | 836          |
    
    
### Evaluation of Results

**BT** and **BT+MRV** algorithms are not the best we can have. BT+MRV is better than BT but both do a lot of assignments as the problem grows. We note specifically that for the 4x4 problem the BT+MRV does a lot more (and much more time respectively) but for the 5x5 problem it does almost half. All three of the above algorithms are forbidden to run a kenken puzzle larger than 5x5, which was shown in practice as the algorithms failed to produce results after too much time.

**FC** and **FC+MRV** algorithms are much better than BT and BT+MRV, since and time and price assignments are much less. Typically we see that for the kenken puzzle 5x5 FC+MRV algorithm finds results with just 40 assignments and 0.00814 seconds, while the BT+MRV algorithm finds the same problem with 330679 assignments and 36.94 seconds. Fewer assignments to the FC and FC+MRV algorithms are reasonable since they do early checks and "delete" inconsistent values for all non-assigned variables.
    
Finally we see that the **MAC** algorithm, as a constraint propagation algorithm, does that very few assignments and therefore very little time. We see that it is equally good with the FC and FC+MRV algorithms.    

Especially in the big kenken puzzles (6x6 and 7x7) we see that the **FC**, **FC+MRV** algorithms and **MAC** are very good and they are the only ones we can have practical with solution to our problems. But the **FC+MRV** and **MAC** algorithms are a little better. Particularly we see that for the while the FC+MRV algorithm does the above assignments much faster in big 6x6 and 7x7 problems, since the MAC algorithm is needed perform above operations/calculations to propagate the constraints.

Καταλήγουμε λοιπόν στο συμπέρασμα ότι οι καλύτεροι αλγόριθμοι για την επίλυση του Kenken puzzle είναι οι αλγόριθμοι **FC**, **FC+MRV** και **MAC**.
    
    
    
## MinConflicts Algorithm
The table shows the time and assignment measurements for the MinCoflicts algorithm:

|                | Time          | Assignments| Results     | 
| :-------------:|:-------------:|:----------:|:-----------:|
|   **3x3**      | 16.53550      | 100013     | None        |
|   **4x4**      | 34.53121      | 100023     | None        |
|   **5x5**      | 58.13730      | 100037     | None        |
|   **6x6**      | -             | -          | -           |
|   **7x7**      | -             | -          | -           |
    
    
  - **-** means that the algorithm failed to finish in a reasonable amount of time space
  - **None** means that the algorithm failed to produce results after a specified number of steps
    
From the results we see in the table above we can deduce that the **MinConflicts** algorithm is the worst since it does most of the time and most assignments because it simply assigns prices to have the least conflicts, but without any control, and can thus be rejected individually solutions that lead him faster. Due to the threshold/threshold of 100,000 (+ some of the function call) steps The algorithm overrides and stops it. So we see that it is not very useful as it takes too much time, lots of steps and finds no effect. 
 
 
## Execution 
To execute the program you can type:
`python3 kenken_csp.py`

If you don't have python 3 in your system you can install it by typing:
`sudo apt install python3.7`
