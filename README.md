# Minesearch in Minesweeper

## Algorithm A: AI-0

### Description

This algorithm finds the bomb through two kind of behaviors. The first one is investigative and it
is actuated when the algorithms has already some information on where the bombs might be,
therefore it investigates those squares until the bomb is found. The second behavior is
explorative, and it is actuated when the algorithm has absolutely no clue of where the bombs
might be, so it just probes the board to find clues, this probing can happen either randomly or in
an orderly manner to improve efficiency at low bomb densities (design chosen).

The algorithm maintains three different mappings of the board, the first one is an untainted map
of the values returned by the board when mined. The second one is a knowledge map that
contains the flag assigned to each square (S = safe, M = mined, U = unknown/not mined, X =
bomb) and its risk score (the sum of the mined value of all the surrounding mined squares) if the
flag is U or the mined value if the flag is M. The third map is a knowledge gain map which
contains the amount of knowledge that would be gained by mining a specific square. If we mine
an isolated square with 8 not mined squares around it, then we would gain more knowledge
about 9 squares, the one mined plus the 8 neighbors, however if we mine a similar square that
has instead 3 square that we are certain already that they are safe, then the knowledge gained
from mining such square would only be 6.

The first square mined is always the “safe” square, and the value returned by the board is then
incorporated in the AI knowledge maps through an update by calling `updateProcedure()`.

```python
def updateProcedure(self):
        self.offsetMinedValues()
        self.updateKnowledge()
        self.updateKnowledgeGain()
        self.getNextMove()
```

The first item in the update process is `offsetMinedValues()` which offsets the mined values in the
knowledge map if a mine was found nearby. Therefore, if a mined square tells us that there are 3
mines nearby, and we already found one, then `offsetMinedValues()` will offset that mined value
from 3 to 2 so that the knowledge map maintains risk scores that are solely based on mines that
have not been found just yet. This step requires _O(nm)_ time where _n_ is the number of rows and _m_
the number of columns.

The second item of the update procedure is `updateKnowledge()` which updates the knowledge
map risk scores and flags by integrating the newly offset mined values and the mined value
returned by the board after mining a square. This step requires _O(nm)_ time.


The third item of the update procedure is `updateKnowledgeGain()` which updates the knowledge
gain map based on how many unexplored squares are nearby and traverses the whole board to
compute lists of possible next moves. This step requires _O(nm)_ time.

At this point the board, from the AI view, would look like the following after mining the safe
square:

![AI-0 Board View](/figures/ai-board-view.jpg "AI Board View")

The last step of the update is then `getNextMove()` which decides what kind of behavior is best to
actuate and from there pick the next square to mine. The AI will always prefer an investigative
behavior, therefore if it has some clues on where some bombs might be, it will go hunting them
down, by selecting the square with the highest risk score as the next square to open. In case of a
tie, the AI will then select the square with the highest risk score and with the highest knowledge
gain, so to also maximize the knowledge gain for the next update. When there are no clues on
where the mines might be (all the U squares have a 0 risk score), then the algorithm will switch
to an explorative behavior, which actually has two sub-behaviors: orderly probing and random
probing. The orderly probing will probe the board in an orderly manner by probing squares at
regular intervals (2 squares apart), traversing the board left to right, top to bottom. This behavior
increases the performance (only on boards with lower bomb density where random approaches
would be less efficient) by minimizing the creation of many low-knowledge gain isolated squares
that a random probing would cause. Both approaches still always pick the square with the highest
knowledge gain, and the AI will pick the approach that guarantees the maximum knowledge gain
(9). In case of a tie, the orderly probing will be picked as it is a smarter way to probe the board in
the long term, but if it cannot offer a knowledge gain of at least 9, then the random probing will
be in charge.
It is necessary to specify that the AI, when selecting the next square to open, will always and
only consider the squares that have the U flag.

![Orderly vs randomly probing board comparison](/figures/orderly-vs-randomly-probing.jpg)

These two images show the AI playing on a 30x30 board with a very low density (only 1 bomb
present at 16|20). The image on the left is the AI with the orderly probing enabled, while the one
on the right has the orderly probing option disabled. We can notice how, in the long run, solely
relaying on random probing (image on the right) can result in the creation of many small patches
of low-knowledge gain squares that reduce the knowledge gain generated by each mining if the
AI got unlucky enough to not accidentally hit the bomb earlier on. In fact such a cluttered
(random) pattern will over time degrade the explorative knowledge gain of each consecutive
mining, while the AI version on the left will always guarantee a +9 knowledge gain for each
mining (except for the very end where it has to deal with those patches inevitably generated by
the misalignment of the first mining at the “safe” square (19|15) if the “safe” square was not
conveniently aligned with the mining pattern of the orderly probing algorithm).

If there is a pool of squares with the same risk score and knowledge gain, then one of these
squares is randomly selected to be the next one to be mined. This step requires _O(1)_ time.

### Justification of correctness

This AI will always find all the bombs as it designed to mine all the squares where it suspects a
bomb is located as to confirm their locations and keep making accurate predictions on where the
remaining bombs are (removing the uncertainty about the correctness of the location). The AI
will keep playing, looking for bombs until all the bombs have been discovered, even to the cost
of mining every square of the board.

### Asymptotic, worst-case runtime analysis

All the steps in `updateProcedure()` (except `getNextMove()` ) need to traverse the whole board to
update the maps, so they will run in _O(nm)_ time where _n_ is the number of rows and _m_ the
number of columns. However each of these steps needs to be run only once, so the
`updateProcedure()` also runs in _O(nm)_ time.

Since we need to do an update of the maps every time we mine a new square, and since this
algorithm needs to confirm the presence of each bomb, then the worst case scenario would be the
case of a n x m board with 100% bomb density, case in which the AI will need to open each
square ( _nm_ squares) and perform an update for each one of them in _O(nm)_ time, therefore the
worst case running time would be **_O((nm)^2)_**.

![25 chronological snapshots of AI-0’s board view while playing on a 10x10 board with 10% bomb density — 33 minings (33% of the board) were necessary to find all the 10 bombs](/figures/ai-search-chronology.png)


## Algorithm B: AI-1

### Description

This algorithm is an alteration of the Naive Single Point algorithm. It uses three sets of
coordinates to base the decision making off of, a set of squares that we know are safe, a set of
squares that we know are bombs and a set of squares to explore that may likely have a bomb in
it.
For each square in the set to explore we use two strategies to determine if there is a bomb nearby.
If a square is opened and it is a bomb, it is a bomb, it is added to the list of bombs and we move
on to another square from the explore list. If the length of the bombs list is equal to the number
of bombs on the board we can return the list. If a square is opened and it has a value of 0, we
know that there are no bombs around the eight squares surrounding the opened square, so all the
surrounding squares are added to the safe list (if they are not already there). If these squares are
in the explore list they can be removed. This lets us know that we do not need to explore these
squares. This strategy is detailed in the Becerra paper, defining the square as an AFN, or all free
neighbors. If the square does not have a value of 0 or 9, then we use an alteration of the AMN or
all marked neighbors strategy described in the Becerra paper. First, we determine the number of
unopened squares that surround the current square we are exploring. If the number of unopened
squares is equal to the value of the current square, accounting for neighboring bombs that are
already opened, we know that all neighbors are bombs and can be added to the list of bombs. If
these squares are in the explore list they can be removed. Otherwise, all of the neighbors are
added to the list of squares to explore.
We continue to explore each square in the explore list until all bombs are found or the explore
list is exhausted. If the list is exhausted we select a random unopened square to explore that is
not in the safe list or bomb list, as we already know the outcome of those squares.

### Justification of correctness

This algorithm will continue to explore the board until every bomb is found. It begins with
adding the initially known safe square to the explore list. After the method is called, it will
always return another square to open, if all bombs are found. If the explore list is empty, an
unopened square whose value cannot be predicted based on the information we have, is
randomly selected and added to the explore list. It is impossible for a square to not be added to
the explore list after an execution of the method without all bombs being found.


### Asymptotic, worst-case runtime analysis

The runtime of executing this algorithm once is _O(1)_. The time it takes to explore each square is
constant. If the square explored is a bomb, it just has to be added to the list of bombs which is
constant. Otherwise all unopened neighbors are added to either the bomb list, the safe list or the
explore list, which also takes constant time. The worst case time it can take to find all of the
bombs is _O(nm)_ where is _n_ is the number of the rows and _m_ is the number of columns in the
board. The best case time it can take to find all of the bombs is _O(n)_ where _n_ is the number of
bombs present on the board.


## AI-0 vs AI-1 comparison

### Testing methodology

Both algorithms have been tested with all the varied density and varied size test cases provided,
and the number of minings and runtime was measured for each test played. Each test case was
played by each algorithm 5 times (to average out lucky random guesses or unlucky sequences of
moves). All the trials’s results were then averaged altogether for a given board size or bomb
density, therefore each data point in the graphs is the average of a total of 25 trials, where 5
different boards (with either same size or density) got played 5 different times.

### Varied Grid Area

![AI-0 and AI-1 runtime/performace vs grid area graph](/figures/runtime-performace-vs-grid.png)

These two graphs have on the common x-axis the area of the board played. The first graph has on
the y-axis the time in seconds taken by the AIs to play the whole board (the lower the better),
while the second graph has on the y-axis the performance of the AIs as percentage of squares
mined (the lower the better).

It can be noticed right away that AI-1 has a much lower (and more slowly growing) runtime.
However AI-0 takes advantage of the extra computing time taken to compute a better playing
strategy and making smarter choices, in fact AI-0 has a better (and more constant and
predictable) performance as it can be seen in the second graph, where AI-0 needs to open fewer
squares to identify all the bombs present on the board.

### Varied Bomb Density

![AI-0 and AI-1 runtime/performace vs bomb density area graph](/figures/runtime-performace-vs-density.png)

These two graphs have on the common x-axis the bomb density of the board played as a
percentage of the grid area. The first graph has on the y-axis the time in seconds taken by the AIs
to play the whole board (the lower the better), while the second graph has on the y-axis the
performance of the AIs as percentage of squares mined (the lower the better).

These two graphs repeat what the previous graphs have shown already, which is that AI-0 has an
greater runtime, but also better performance, while AI-1 solves the game much faster, but at a
greater cost of mined squares. However in these two graphs we can see that the bomb density
affects the performance and runtime of the algorithms more linearly compared to the grid size.

Overall, how already suggested in the runtime analyses, the grid size has a major impact on the
runtime of both AIs rather than their performance, while bomb density instead, mainly affects the
performance rather than the runtime of the AIs.

## Original README

```
========================= Collaborations =========================

> Andrea Covre
    andrea.covre@gatech.edu

> Parisha Reddy
    parisha@gatech.edu

============================ Files =============================

> README.md/.txt
    description:    document that explains the design, 
                    correctness, and runtime analysis of both 
                    AIs, and compares their performance and 
                    runtime against both grid area and bomb 
                    density.

        authors:    Andrea Covre


> AI_0.py
    description:    contains the class that defines our first 
                    AI, it finds bombs based on risk score, 
                    knowledge gain and minimized probing 
                    overlap.

        authors:    Andrea Covre


> AI_1.py
    description:    contains the class that defines our second 
                    AI, it is based on the naive single point 
                    algorithm described in the "Algorithmic 
                    Approaches to Playing Minesweeper" thesis by
                    David Becerra.

        authors:    Parisha Reddy


> minesweeper.py
    description:    game engine and controller where AIs and 
                    Boards are instantiated and executed.

        authors:    Andrea Covre


> Board.py
    description:    class that takes in a JSON file, parses it, 
                    stores all the related information about the
                    board that is being played, manages the 
                    mining and counts the accesses.

        authors:    Andrea Covre


======================== Instructions ==========================

From the command line and inside the project directory run the 
following:

    python minesweeper.py <JSON test file>

where <JSON test file> represents the name (or relative path) of
a JSON file (within the project directory) that represents a 
minesweeper board with the proper formatting.

Such command will make both AIs (AI-0 and AI-1) play one full 
game from start to finish on the board specified. The board 
information will be printed out along with the execution time, 
number of board accesses, percentage mined and bombs locations
from both AIs.

Python version required: 3.9.1
```


