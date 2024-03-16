import streamlit as st
import random
from collections import Counter
from itertools import combinations, cycle
from math import comb

def simulate_scores(team1_scores, team2_scores, simulations=10000):
    simulated_scores = [(random.choice(team1_scores), random.choice(team2_scores)) for _ in range(simulations)]
    return simulated_scores

def calculate_statistics(simulated_scores):
    total_scores = [sum(scores) for scores in simulated_scores]
    avg_score = sum(total_scores) / len(total_scores)
    highest_score = max(total_scores)
    lowest_score = min(total_scores)
    score_freq = Counter(total_scores)
    most_common_score_total, occurrences = score_freq.most_common(1)[0]
    return avg_score, highest_score, lowest_score, total_scores, (most_common_score_total, occurrences)

def analyze_over_under(total_scores, overs, unders):
    results = {}
    for over in overs:
        over_count = sum(score > over for score in total_scores)
        over_percentage = (over_count / len(total_scores)) * 100
        results[f'over {over}'] = (over_count, over_percentage)
    for under in unders:
        under_count = sum(score < under for score in total_scores)
        under_percentage = (under_count / len(total_scores)) * 100
        results[f'under {under}'] = (under_count, under_percentage)
    return results

def generate_evenly_distributed_parlays(events):
    parlays = []
    event_count = len(events)
    total_parlays = comb(event_count, 2)
    event_cycle = cycle(events)
    used_pairs = set()
    
    while len(parlays) < total_parlays:
        for i in range(event_count):
            base_event = next(event_cycle)
            for j in range(1, event_count):
                pairing_event = events[(i + j) % event_count]
                if (base_event, pairing_event) not in used_pairs and (pairing_event, base_event) not in used_pairs:
                    parlays.append((base_event, pairing_event))
                    used_pairs.add((base_event, pairing_event))
                    if len(parlays) == total_parlays:
                        break
            if len(parlays) == total_parlays:
                break
    return parlays

st.title('Sports Score Simulation & 2-Bet Parlay')

tab1, tab2 = st.tabs(["Score Simulation", "2-Bet Parlay"])

with tab1:
    team1_name = st.text_input("Enter the first team name:", key='team1_name')
    team2_name = st.text_input("Enter the second team name:", key='team2_name')
    team1_scores = st.text_input("Enter the scores for team 1 separated by space:", key='team1_scores')
    team2_scores = st.text_input("Enter the scores for team 2 separated by space:", key='team2_scores')
    overs = [st.number_input("Enter first 'over' value (optional):", step=1, key='over1'),
             st.number_input("Enter second 'over' value (optional):", step=1, key='over2')]
    unders = [st.number_input("Enter first 'under' value (optional):", step=1, key='under1'),
              st.number_input("Enter second 'under' value (optional):", step=1, key='under2')]

    if st.button('Simulate and Analyze', key='analyze_simulation'):
        if team1_scores and team2_scores:
            team1_scores = list(map(int, team1_scores.split()))
            team2_scores = list(map(int, team2_scores.split()))

            simulated_scores = simulate_scores(team1_scores, team2_scores)
            avg_score, highest_score, lowest_score, total_scores, most_common_score_total = calculate_statistics(simulated_scores)

            st.write(f"Average Total Score: {avg_score:.2f}")
            st.write(f"Highest Score: {highest_score}")
            st.write(f"Lowest Score: {lowest_score}")
            st.write(f"Most Likely Total Score: {most_common_score_total[0]} occurring {most_common_score_total[1]} times")

            overs = [over for over in overs if over > 0]
            unders = [under for under in unders if under > 0]
            
            results = analyze_over_under(total_scores, overs, unders)
            for key, (count, percentage) in results.items():
                st.write(f"- Final score went {key} {count} times ({percentage:.2f}% of the time).")

with tab2:
    st.subheader("2-Bet Parlay Generator")
    events = [st.text_input(f"Enter game event {i+1} (leave blank if not used):", key=f'parlay_event{i+1}') for i in range(10)]
    events = [event for event in events if event]

    if st.button('Generate Evenly Distributed Parlays', key='generate_even_parlays'):
        if len(events) >= 2:
            parlays = generate_evenly_distributed_parlays(events)
            st.write(f"Generated {len(parlays)} evenly distributed 2-bet parlays:")
            for i, parlay in enumerate(parlays, start=1):
                st.write(f"{i}. {parlay[0]} / {parlay[1]}")
        else:
            st.write("Please enter at least 2 game events to generate parlays.")
