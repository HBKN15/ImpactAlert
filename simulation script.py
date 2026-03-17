import numpy as np
import time
import os

# --- CONFIGURATION (Edit these values) ---
CONFIG = {
    "WIDTH": 8,            # Number of columns
    "HEIGHT": 8,           # Number of rows
    "MIN_DIST": 50,        # Minimum distance in mm
    "MAX_DIST": 5000,      # Maximum distance in mm
    "REFRESH_RATE": 0.2,   # Delay between frames (seconds)
    "OBJ_SIZE": 2,         # Size of the moving object (e.g., 2x2)
    "USE_COLORS": True     # Toggle terminal color output
}

class ObjectTracker:
    """Manages the state of the simulated object to ensure smooth movement."""
    def __init__(self):
        # Start in the middle
        self.x = CONFIG["WIDTH"] // 2
        self.y = CONFIG["HEIGHT"] // 2
        # Start at a medium distance
        self.dist = 1000 

    def update_position(self):
        """Moves the object to an adjacent cell (up, down, left, right, or stay)."""
        # Move X (-1, 0, or 1)
        self.x += np.random.choice([-1, 0, 1])
        # Move Y (-1, 0, or 1)
        self.y += np.random.choice([-1, 0, 1])
        
        # Move Distance smoothly (+/- 50mm)
        self.dist += np.random.randint(-100, 101)

        # Boundary constraints
        self.x = max(0, min(CONFIG["WIDTH"] - CONFIG["OBJ_SIZE"], self.x))
        self.y = max(0, min(CONFIG["HEIGHT"] - CONFIG["OBJ_SIZE"], self.y))
        self.dist = max(CONFIG["MIN_DIST"], min(2500, self.dist)) # Keep object in detectable range

def clear_terminal():
    """Clears the terminal screen for Windows and Linux."""
    os.system('cls' if os.name == 'nt' else 'clear')

def initialize_windows_ansi():
    """Enables ANSI color support for Windows Command Prompt/PowerShell."""
    if os.name == 'nt':
        os.system('')

def generate_tof_frame(tracker):
    """
    Calculates a single matrix frame based on the tracker's current state.
    """
    w, h = CONFIG["WIDTH"], CONFIG["HEIGHT"]
    min_d, max_d = CONFIG["MIN_DIST"], CONFIG["MAX_DIST"]
    
    # Update the object's physical state
    tracker.update_position()
    
    # 1. Background: Distant values with noise
    matrix = np.random.randint(max_d - 100, max_d + 1, size=(h, w))

    # 2. Draw Object: Insert the object based on tracker state
    size = CONFIG["OBJ_SIZE"]
    for i in range(tracker.y, tracker.y + size):
        for j in range(tracker.x, tracker.x + size):
            # Ensure we don't index out of bounds (extra safety)
            if i < h and j < w:
                matrix[i, j] = tracker.dist

    return np.clip(matrix, min_d, max_d)

def print_matrix(matrix):
    """Formats and prints the matrix with depth-based coloring."""
    clear_terminal()
    print(f"--- ToF Simulator [{CONFIG['WIDTH']}x{CONFIG['HEIGHT']}] ---")
    print(f"Range: {CONFIG['MIN_DIST']}mm - {CONFIG['MAX_DIST']}mm\n")
    
    for row in matrix:
        formatted_row = []
        for val in row:
            if CONFIG["USE_COLORS"]:
                if val < 500:
                    color = "\033[91m"    # Red (Very Close)
                elif val < 1500:
                    color = "\033[93m"    # Yellow (Mid Range)
                elif val < 3000:
                    color = "\033[96m"    # Cyan (Far)
                else:
                    color = "\033[90m"    # Gray (Background)
                
                formatted_row.append(f"{color}{val:4}\033[0m")
            else:
                formatted_row.append(f"{val:4}")
        
        print("  ".join(formatted_row))
    
    print("\n[Ctrl+C] to stop simulation")

def main():
    initialize_windows_ansi()
    tracker = ObjectTracker()
    try:
        while True:
            frame = generate_tof_frame(tracker)
            print_matrix(frame)
            time.sleep(CONFIG["REFRESH_RATE"])
    except KeyboardInterrupt:
        print("\n\nSimulation terminated by user.")

if __name__ == "__main__":
    main()