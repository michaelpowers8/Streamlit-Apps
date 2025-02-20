import streamlit as st
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def tower_of_hanoi(n: int, source: str = 'A', auxiliary: str = 'B', destination: str = 'C') -> list:
    """
    Compute the list of moves to solve the Tower of Hanoi puzzle.
    Each move is a tuple (from_peg, to_peg).
    """
    moves = []
    def solve(n: int, source: str, auxiliary: str, destination: str):
        if n == 1:
            moves.append((source, destination))
        else:
            solve(n - 1, source, destination, auxiliary)
            moves.append((source, destination))
            solve(n - 1, auxiliary, source, destination)
    solve(n, source, auxiliary, destination)
    return moves

def draw_towers(state: dict, num_disks: int, moving_disk: int = None, moving_disk_pos: tuple = None) -> plt.Figure:
    """
    Draw the three towers with disks using matplotlib.
    
    - state: a dict mapping each peg ('A','B','C') to a list of disks.
      Disks are represented as integers (with larger numbers meaning larger disks).
    - moving_disk: if provided, the disk value that is currently moving.
    - moving_disk_pos: a tuple (x, y) indicating the center position of the moving disk.
    """
    # Define peg x-positions and drawing parameters
    peg_positions = {"A": 1, "B": 3, "C": 5}
    disk_height = 0.4
    min_width = 0.5
    max_width = 1.5

    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Draw pegs (vertical lines)
    for peg, x in peg_positions.items():
        ax.plot([x, x], [0, 6], color="black", linewidth=3)
        ax.text(x, 6.2, peg, ha='center', va='bottom', fontsize=12)
    
    # Draw disks on each peg
    for peg, disks in state.items():
        x_center = peg_positions[peg]
        # Disks are stacked from bottom (index 0) upward.
        for i, disk in enumerate(disks):
            y = i * disk_height
            # Compute disk width: smallest disk (value 1) gets min_width,
            # largest disk (value num_disks) gets max_width.
            if num_disks > 1:
                width = min_width + (disk - 1) / (num_disks - 1) * (max_width - min_width)
            else:
                width = (min_width + max_width) / 2
            rect = patches.Rectangle((x_center - width/2, y), width, disk_height,
                                     facecolor="skyblue", edgecolor="black")
            ax.add_patch(rect)
            ax.text(x_center, y + disk_height/2, str(disk), ha='center', va='center', fontsize=10)
    
    # Draw the moving disk (if any) with a different color
    if moving_disk is not None and moving_disk_pos is not None:
        x_m, y_m = moving_disk_pos
        if num_disks > 1:
            width = min_width + (moving_disk - 1) / (num_disks - 1) * (max_width - min_width)
        else:
            width = (min_width + max_width) / 2
        rect = patches.Rectangle((x_m - width/2, y_m), width, disk_height,
                                 facecolor="orange", edgecolor="red")
        ax.add_patch(rect)
        ax.text(x_m, y_m + disk_height/2, str(moving_disk), ha='center', va='center', fontsize=10, color="black")
    
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 7)
    ax.axis("off")
    return fig

def animate_move(state: dict, disk: int, source: str, destination: str, num_disks: int, 
                 animation_placeholder, disk_height: float = 0.4):
    """
    Animate the movement of a disk from the source peg to the destination peg.
    The animation is split into three phases: vertical up, horizontal, vertical down.
    """
    peg_positions = {"A": 1, "B": 3, "C": 5}
    
    # Compute start and end positions for the moving disk.
    # (Note: state[source] already had the disk popped.)
    old_source_length = len(state[source]) + 1  # before removal
    start_y = old_source_length * disk_height
    final_y = len(state[destination]) * disk_height  # disk will land on top of current disks
    
    start_x = peg_positions[source]
    end_x = peg_positions[destination]
    
    # Define a fixed top height for the vertical upward movement.
    top_y = 6
    
    # Number of frames per phase
    frames_up = 10
    frames_horizontal = 10
    frames_down = 10
    
    # Phase 1: Vertical up movement
    for y in np.linspace(start_y, top_y, frames_up):
        fig = draw_towers(state, num_disks, moving_disk=disk, moving_disk_pos=(start_x, y))
        animation_placeholder.pyplot(fig)
        time.sleep(0.05)
    
    # Phase 2: Horizontal movement at the top height
    for x in np.linspace(start_x, end_x, frames_horizontal):
        fig = draw_towers(state, num_disks, moving_disk=disk, moving_disk_pos=(x, top_y))
        animation_placeholder.pyplot(fig)
        time.sleep(0.05)
    
    # Phase 3: Vertical down movement
    for y in np.linspace(top_y, final_y, frames_down):
        fig = draw_towers(state, num_disks, moving_disk=disk, moving_disk_pos=(end_x, y))
        animation_placeholder.pyplot(fig)
        time.sleep(0.05)
    
    # Final frame (disk landed)
    fig = draw_towers(state, num_disks)
    animation_placeholder.pyplot(fig)
    time.sleep(0.05)

def main():
    st.title("Tower of Hanoi Animation with Sliding Disks")
    st.write("Watch the disks slide between towers as the solution is animated.")
    
    num_disks = st.slider("Select the number of disks", min_value=1, max_value=8, value=3)
    moves = tower_of_hanoi(num_disks)
    
    # Initialize the state: All disks start on peg A (largest at bottom).
    state = {
        "A": list(range(num_disks, 0, -1)),  # e.g., [3, 2, 1] for 3 disks
        "B": [],
        "C": []
    }
    
    animation_placeholder = st.empty()
    sidebar_placeholder = st.sidebar.empty()
    
    # Render the full moves list in the sidebar
    def render_moves(moves, current_move_index=-1):
        out = "### Moves List\n"
        for i, move in enumerate(moves):
            if i == current_move_index:
                out += f"> **{i+1}. Move from {move[0]} to {move[1]}**\n"
            else:
                out += f"{i+1}. Move from {move[0]} to {move[1]}\n"
        return out
    
    sidebar_placeholder.markdown(render_moves(moves))
    
    # Draw the initial towers
    fig = draw_towers(state, num_disks)
    animation_placeholder.pyplot(fig)
    
    if st.button("Start Animation"):
        # Animate each move
        for i, move in enumerate(moves):
            # Update sidebar highlighting the current move.
            sidebar_placeholder.markdown(render_moves(moves, current_move_index=i))
            time.sleep(0.05)
            source, dest = move
            # Pop the top disk from the source peg.
            disk = state[source].pop()
            # Animate the sliding move.
            animate_move(state, disk, source, dest, num_disks, animation_placeholder)
            # After animation, append the disk to the destination peg.
            state[dest].append(disk)
            
        
        # Final update to show completed state.
        fig = draw_towers(state, num_disks)
        animation_placeholder.pyplot(fig)
        sidebar_placeholder.markdown(render_moves(moves, current_move_index=len(moves)))
        
if __name__ == "__main__":
    main()
