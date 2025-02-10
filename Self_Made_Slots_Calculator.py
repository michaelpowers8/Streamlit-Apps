import streamlit as st
import hashlib
import hmac
import random
import string

def sha256_encrypt(input_string: str) -> str:
    return hashlib.sha256(input_string.encode('utf-8')).hexdigest()

def generate_seed(length=64):
    return ''.join(random.choices(string.hexdigits, k=length))

def seeds_to_hexadecimals(server_seed, client_seed, nonce):
    messages = [f"{client_seed}:{nonce}:{x}" for x in range(2)]
    return [hmac.new(server_seed.encode(), msg.encode(), hashlib.sha256).hexdigest() for msg in messages]

def hexadecimal_to_bytes(hexadecimal):
    return list(bytes.fromhex(hexadecimal))

def bytes_to_number(bytes_list, weights):
    number = sum(float(bytes_list[i]) / float(256 ** (i + 1)) for i in range(4))
    cumulative_weights = [sum(weights[:i+1]) for i in range(len(weights))]
    total_weight = cumulative_weights[-1]
    weighted_number = number * total_weight
    for i, weight in enumerate(cumulative_weights):
        if weighted_number <= weight:
            return i
    return len(weights) - 1

def seeds_to_results(server_seed, client_seed, nonce):
    prizes = ['cherry', 'lemon', 'bell', 'clover', 'diamond', 'star', 'caterpillar', 'butterfly', 'angel_butterfly']
    weights = [0.2, 0.18, 0.15, 0.13, 0.12, 0.1, 0.07, 0.045, 0.005]
    hexs = seeds_to_hexadecimals(server_seed, client_seed, nonce)
    bytes_lists = [hexadecimal_to_bytes(h) for h in hexs]
    rows = []
    for bytes_list in bytes_lists:
        row = [prizes[bytes_to_number(bytes_list[i:i+4], weights)] for i in range(0, len(bytes_list), 4)][:3]
        rows.append(row)
    return rows

def check_for_wins(rows):
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
