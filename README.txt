Submitted on May 2nd, 2021

========================= Team Members =========================

> Andrea Covre
    andrea.covre@gatech.edu

> Parisha Reddy
    parisha@gatech.edu

============================ Files =============================

> Project_Report.pdf
    description:    document that explains the design, 
                    correctness, and runtime analysis of both 
                    AIs, and compares their performance and 
                    runtime against both grid area and bomb 
                    density.

        authors:    Andrea Covre
                    Parisha Reddy


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