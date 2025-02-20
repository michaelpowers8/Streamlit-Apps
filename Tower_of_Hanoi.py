import streamlit as st
import time

def tower_of_hanoi(n: int, source: str = 'A', auxiliary: str = 'B', destination: str = 'C') -> list:
    """
    Compute the Tower of Hanoi solution moves.
    
    Returns a list of tuples representing moves (from_peg, to_peg).
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

def render_state(state: dict) -> str:
    """
    Create a markdown representation of the current state of the pegs.
    """
    out = ""
    for peg in ["A", "B", "C"]:
        # Render disks as a series of blocks; the larger the number, the wider the disk.
        peg_disks = state[peg]
        disk_str = "  ".join(str(disk) for disk in peg_disks) if peg_disks else "Empty"
        out += f"**Peg {peg}:** {disk_str}\n\n"
    return out

def render_moves(moves: list, current: int) -> str:
    """
    Create a markdown list of moves with the current move highlighted.
    
    The current move (index) is highlighted with a marker.
    """
    out = "### Moves List\n"
    for i, move in enumerate(moves):
        if i == current:
            out += f"> **{i+1}. Move from {move[0]} to {move[1]}**\n"
        else:
            out += f"{i+1}. Move from {move[0]} to {move[1]}\n"
    return out

# Streamlit app layout
st.title("Tower of Hanoi Animation")
st.write("This app shows the solution to the Tower of Hanoi puzzle and animates each move.")

# Let the user select the number of disks (keeping the number moderate to avoid long animations)
num_disks = st.slider("Select the number of disks", min_value=1, max_value=8, value=3, step=1)

# Get the list of moves to solve the puzzle
moves = tower_of_hanoi(num_disks)

# Initialize the state: all disks start on peg A (largest at the bottom)
state = {
    "A": list(range(num_disks, 0, -1)),  # e.g., for 3 disks: [3, 2, 1]
    "B": [],
    "C": []
}

# Placeholders for the main animation area and sidebar moves list
animation_placeholder = st.empty()
sidebar_placeholder = st.sidebar.empty()

# Initially, show the complete list of moves with no move highlighted
sidebar_placeholder.markdown(render_moves(moves, current=-1))
animation_placeholder.markdown("### Initial State:\n" + render_state(state))

if st.button("Start Animation"):
    # Reset state when starting
    state = {
        "A": list(range(num_disks, 0, -1)),
        "B": [],
        "C": []
    }
    # Update initial state display
    animation_placeholder.markdown("### Initial State:\n" + render_state(state))
    sidebar_placeholder.markdown(render_moves(moves, current=-1))
    time.sleep(1)
    
    # Animate each move
    for i, move in enumerate(moves):
        source, dest = move
        # Perform the move: pop from source and push onto destination
        disk = state[source].pop()
        state[dest].append(disk)
        
        # Update the main area with the new state
        animation_placeholder.markdown("### Current State:\n" + render_state(state))
        # Update sidebar to highlight the current move
        sidebar_placeholder.markdown(render_moves(moves, current=i))
        
        # Pause so the user can see the change
        time.sleep(1)
    
    # Final state update
    animation_placeholder.markdown("### Final State:\n" + render_state(state))
    sidebar_placeholder.markdown(render_moves(moves, current=len(moves)))
