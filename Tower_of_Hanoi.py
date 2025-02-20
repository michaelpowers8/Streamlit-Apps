import streamlit as st
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def tower_of_hanoi(n: int, source: str = 'A', auxiliary: str = 'B', destination: str = 'C') -> list:
    """Compute the list of moves to solve the Tower of Hanoi puzzle."""
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
    """
    peg_positions = {"A": 1, "B": 3, "C": 5}
    disk_height = 0.25
    min_width = 0.4
    max_width = 1.2

    fig, ax = plt.subplots(figsize=(5, 5))

    # Draw pegs (vertical lines)
    for peg, x in peg_positions.items():
        ax.plot([x, x], [0, 5], color="black", linewidth=2)
        ax.text(x, 5.2, peg, ha='center', va='bottom', fontsize=10)
    
    # Draw disks on each peg
    for peg, disks in state.items():
        x_center = peg_positions[peg]
        for i, disk in enumerate(disks):
            y = i * disk_height
            width = min_width + (disk - 1) / (num_disks - 1) * (max_width - min_width) if num_disks > 1 else (min_width + max_width) / 2
            rect = patches.Rectangle((x_center - width/2, y), width, disk_height, facecolor="skyblue", edgecolor="black")
            ax.add_patch(rect)
            ax.text(x_center, y + disk_height/2, str(disk), ha='center', va='center', fontsize=8)
    
    # Draw moving disk
    if moving_disk is not None and moving_disk_pos is not None:
        x_m, y_m = moving_disk_pos
        width = min_width + (moving_disk - 1) / (num_disks - 1) * (max_width - min_width) if num_disks > 1 else (min_width + max_width) / 2
        rect = patches.Rectangle((x_m - width/2, y_m), width, disk_height, facecolor="orange", edgecolor="red")
        ax.add_patch(rect)
        ax.text(x_m, y_m + disk_height/2, str(moving_disk), ha='center', va='center', fontsize=8, color="black")
    
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 6)
    ax.axis("off")
    return fig

def animate_move(state: dict, disk: int, source: str, destination: str, num_disks: int, animation_placeholder, disk_height: float = 0.25):
    """Animate a disk moving from source to destination."""
    peg_positions = {"A": 1, "B": 3, "C": 5}
    
    old_source_length = len(state[source]) + 1
    start_y = old_source_length * disk_height
    final_y = len(state[destination]) * disk_height
    start_x = peg_positions[source]
    end_x = peg_positions[destination]
    top_y = 5

    # More frames for smoother animation
    frames_up = 15
    frames_horizontal = 20
    frames_down = 15

    # Phase 1: Move up
    for y in np.linspace(start_y, top_y, frames_up):
        fig = draw_towers(state, num_disks, moving_disk=disk, moving_disk_pos=(start_x, y))
        animation_placeholder.pyplot(fig)
        time.sleep(0.05)

    # Phase 2: Move horizontally
    for x in np.linspace(start_x, end_x, frames_horizontal):
        fig = draw_towers(state, num_disks, moving_disk=disk, moving_disk_pos=(x, top_y))
        animation_placeholder.pyplot(fig)
        time.sleep(0.05)

    # Phase 3: Move down
    for y in np.linspace(top_y, final_y, frames_down):
        fig = draw_towers(state, num_disks, moving_disk=disk, moving_disk_pos=(end_x, y))
        animation_placeholder.pyplot(fig)
        time.sleep(0.05)

    fig = draw_towers(state, num_disks)
    animation_placeholder.pyplot(fig)
    time.sleep(0.05)

def main():
    st.title("Tower of Hanoi Animation (Smooth)")
    st.write("Watch the disks slide smoothly between towers.")

    num_disks = st.slider("Select the number of disks", min_value=1, max_value=8, value=3)
    moves = tower_of_hanoi(num_disks)

    state = {
        "A": list(range(num_disks, 0, -1)),
        "B": [],
        "C": []
    }

    animation_placeholder = st.empty()
    sidebar_placeholder = st.sidebar.empty()

    def render_moves(moves, current_move_index=-1):
        out = "### Moves List\n"
        for i, move in enumerate(moves):
            if i == current_move_index:
                out += f"> **{i+1}. Move from {move[0]} to {move[1]}**\n"
            else:
                out += f"{i+1}. Move from {move[0]} to {move[1]}\n"
        return out

    sidebar_placeholder.markdown(render_moves(moves))
    
    fig = draw_towers(state, num_disks)
    animation_placeholder.pyplot(fig)

    if st.button("Start Animation"):
        for i, move in enumerate(moves):
            source, dest = move
            disk = state[source].pop()
            animate_move(state, disk, source, dest, num_disks, animation_placeholder)
            state[dest].append(disk)
            sidebar_placeholder.markdown(render_moves(moves, current_move_index=i))
            time.sleep(0.05)

        fig = draw_towers(state, num_disks)
        animation_placeholder.pyplot(fig)
        sidebar_placeholder.markdown(render_moves(moves, current_move_index=len(moves)))

if __name__ == "__main__":
    main()
