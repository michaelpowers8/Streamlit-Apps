import streamlit as st
import hashlib
import hmac
import random
import string
from PIL import Image

def sha256_encrypt(input_string:str) -> str:
    return hashlib.sha256(input_string.encode('utf-8')).hexdigest()

def generate_seed(length=64) -> str:
    return ''.join(random.choices(string.hexdigits, k=length))

def seeds_to_hexadecimals(server_seed:str, client_seed:str, nonce:int) -> list[str]:
    messages = [f"{client_seed}:{nonce}:{x}" for x in range(2)]
    return [hmac.new(server_seed.encode(), msg.encode(), hashlib.sha256).hexdigest() for msg in messages]

def hexadecimal_to_bytes(hexadecimal:list[str]) -> list[bytes]:
    return list(bytes.fromhex(hexadecimal))

def bytes_to_number(bytes_list:list[bytes], weights:list[float]):
    number:float = sum(float(bytes_list[i]) / float(256 ** (i + 1)) for i in range(4))
    cumulative_weights:list[float] = [sum(weights[:i+1]) for i in range(len(weights))]
    total_weight:float = cumulative_weights[-1]
    weighted_number:float = number * total_weight
    for i, weight in enumerate(cumulative_weights):
        if weighted_number <= weight:
            return i
    return len(weights) - 1

def seeds_to_results(server_seed:str, client_seed:str, nonce:int, prizes:list[str]):
    weights:list[float] = [0.2, 0.18, 0.15, 0.13, 0.12, 0.1, 0.07, 0.045, 0.005]
    
    hexs:list[str] = seeds_to_hexadecimals(server_seed, client_seed, nonce)
    bytes_lists:list[list[bytes]] = [hexadecimal_to_bytes(h) for h in hexs]
    
    rows:list[list[str]] = []
    current_row:list[str] = []
    
    for bytes_list in bytes_lists:
        for i in range(0, len(bytes_list), 4):
            if len(current_row) == 3:  # When row is filled, add it and start new
                rows.append(current_row)
                current_row = []
            current_row.append(prizes[bytes_to_number(bytes_list[i:i+4], weights)])
    
    if current_row:  # Append last row if incomplete
        rows.append(current_row)
    
    return rows[:3]  # Ensure exactly 3 rows

def check_for_wins(rows:list[list[str]]):
    wins = []
    for row in rows:
        if row[0] == row[1] == row[2]:
            wins.append(row[0])
    for i in range(3):
        if rows[0][i] == rows[1][i] == rows[2][i]:
            wins.append(rows[0][i])
    if rows[0][0] == rows[1][1] == rows[2][2]:
        wins.append(rows[0][0])
    if rows[0][2] == rows[1][1] == rows[2][0]:
        wins.append(rows[0][2])
    return wins

def calculate_wins(wins:list[str], prizes:list[str], bet_amount:int, multipliers:list[float]):
    if(len(wins)==0):
        return 0
    total_multiplier:float = 0
    for win in wins:
        total_multiplier += multipliers[prizes.index(win)]
    return bet_amount*total_multiplier

def display_balance():
    st.write(f"Credits: {st.session_state.balance}")
    st.write(f"Bet Amount: {st.session_state.bet_amount}")
    
def display_seed_information():
    # Custom CSS for the subheader
    st.markdown("""
            <style>
            .custom-subheader {
                font-size: 24px; /* Change this value to customize the size */
                font-weight: bold; /* Change this to 'normal' if you don't want bold */
                color: #ff5733; /* Change this value to customize the color */
                white-space: nowrap; /* Prevent word wrap */
            }
            </style>
        """, unsafe_allow_html=True)

    # Apply the custom CSS class to your subheader
    st.markdown(f'''<p class="server-seed-hashed">Server Seed (Hashed): {st.session_state.server_seed_hashed}\n</p>''', unsafe_allow_html=True)
    st.markdown(f'''<p class="client-seed">Client Seed: {st.session_state.client_seed}</p>''', unsafe_allow_html=True)
    st.markdown(f'''<p class="nonce">Nonce: {st.session_state.nonce}</p>''', unsafe_allow_html=True)
    
def display_images(results:list[str]):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(st.session_state.images[st.session_state.prizes.index(results[0][0])])
        st.image(st.session_state.images[st.session_state.prizes.index(results[1][0])])
        st.image(st.session_state.images[st.session_state.prizes.index(results[2][0])])
    with col2:
        st.image(st.session_state.images[st.session_state.prizes.index(results[0][1])])
        st.image(st.session_state.images[st.session_state.prizes.index(results[1][1])])
        st.image(st.session_state.images[st.session_state.prizes.index(results[2][1])])
    with col3:
        st.image(st.session_state.images[st.session_state.prizes.index(results[0][2])])
        st.image(st.session_state.images[st.session_state.prizes.index(results[1][2])])
        st.image(st.session_state.images[st.session_state.prizes.index(results[2][2])])

def update_screen():
    display_seed_information()
    display_images(st.session_state.results)  # Use session_state.results
    display_balance()

st.header("Fluttering Riches - Slot Machine")
# Ensure results persist in session state
if "results" not in st.session_state:
    st.session_state.server_seed = generate_seed() 
    st.session_state.server_seed_hashed = sha256_encrypt(st.session_state.server_seed)
    st.session_state.client_seed = generate_seed(20)
    st.session_state.nonce = 1
    st.session_state.prizes = [
                                    'cherry', 'lemon', 'bell', 
                                    'clover', 'diamond', 'star', 
                                    'caterpillar', 'butterfly', 'angel_butterfly'
                                ]
    st.session_state.images = [
                                    Image.open('cherry.jpg'),Image.open('lemon.jpg'),Image.open('bell.jpg'),
                                    Image.open('clover.jpg'),Image.open('diamond.jpg'),Image.open('star.jpg'),
                                    Image.open('caterpillar.jpg'),Image.open('butterfly.jpg'),Image.open('angel_butterfly.jpg')
                                ]
    st.session_state.multipliers = [1.3, 2.25, 3.00, 5.00, 10.0, 25.0,  50.0, 125.0, 5000]
    st.session_state.nonce = 0
    st.session_state.balance = 10_000
    st.session_state.results = seeds_to_results(
            st.session_state.server_seed, 
            st.session_state.client_seed, 
            st.session_state.nonce,
            st.session_state.prizes
        )
    st.session_state.nonce += 1
    update_screen()

st.session_state.bet_amount = st.number_input("Bet Amount:", min_value=0, max_value=st.session_state.balance)

if st.button("Spin"):
    if st.session_state.balance >= st.session_state.bet_amount:
        st.session_state.balance -= st.session_state.bet_amount
        st.session_state.results = seeds_to_results(
                st.session_state.server_seed, 
                st.session_state.client_seed, 
                st.session_state.nonce,
                st.session_state.prizes
            )
        st.session_state.nonce += 1
        wins = check_for_wins(st.session_state.results)
        if wins:
            st.session_state.balance += int(
                calculate_wins(wins, st.session_state.prizes, st.session_state.bet_amount, st.session_state.multipliers)
            )
        update_screen()
    else:
        st.error("Insufficient balance!")

update_screen()  # Ensure UI updates correctly