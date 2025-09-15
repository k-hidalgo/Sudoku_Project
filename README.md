**Simplified Sudoku (PyGame)**

**Overview**
This project is a simplified Sudoku game built using Python and PyGame. 

The game provides:
- A **PyGame-based user interface** for interaction.  
- Functionality to **input numbers**, check validity, and manage the flow of the game.  
- A simplified set of Sudoku rules (smaller grid size, reduced constraints) to make the game easier to play and implement.  

---

**How It Works**
- The board is displayed using **PyGame** with a clean grid layout.  
- Players click on a cell and type a number to make a move.  
- The game checks the move for validity according to Sudoku rules:  
  - No repeated numbers in the same row.  
  - No repeated numbers in the same column.  
  - No repeated numbers in the same region (depending on the simplified grid size).  
- The interface updates in real time with player inputs.  
- The game ends when the board is completely and correctly filled.  

---

Technologies Used
- **Python 3**  
- **PyGame** (for the UI and event handling)  
