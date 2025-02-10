import streamlit as st
import hashlib
import hmac
import random
import string

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

def seeds_to_results(server_seed:str, client_seed:str, nonce:int):
    prizes:list[str] = ['cherry', 'lemon', 'bell', 'clover', 'diamond', 'star', 'caterpillar', 'butterfly', 'angel_butterfly']
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

st.title("Fluttering Riches - Slot Machine")
if 'server_seed' not in st.session_state:
    st.session_state.server_seed = generate_seed()
    st.session_state.client_seed = generate_seed(20)
    st.session_state.nonce = 1
    st.session_state.balance = 10000
    st.session_state.bet_amount = 200

st.write(f"Credits: {st.session_state.balance}")
st.write(f"Bet Amount: {st.session_state.bet_amount}")
if st.button("Spin"):
    if st.session_state.balance >= st.session_state.bet_amount:
        st.session_state.balance -= st.session_state.bet_amount
        results = seeds_to_results(st.session_state.server_seed, st.session_state.client_seed, st.session_state.nonce)
        st.session_state.nonce += 1
        for row in results:
            st.write(" | ".join(row))
        wins = check_for_wins(results)
        if wins:
            st.success(f"You won with: {', '.join(wins)}!")
    else:
        st.error("Insufficient balance!")
