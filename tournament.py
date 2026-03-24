#!/usr/bin/env python3
"""Badminton round-robin tournament (X teams, best of 3 games per match)."""
from itertools import combinations

def get_team_names():
    print("Enter team names, one per line. Blank line to finish.")
    print("Example: Ashok and Manisha")
    teams = []
    idx = 1
    while True:
        name = input(f"Team {idx} name (or blank to stop): ").strip()
        if not name:
            break
        teams.append(name)
        idx += 1

    if len(teams) < 2:
        print("At least 2 teams are required. Using default teams: Team1, Team2, Team3.")
        return ["Team1", "Team2", "Team3"]

    return teams


def get_game_winner(team_a, team_b, game_idx):
    while True:
        resp = input(f"Game {game_idx + 1}: winner ({team_a}/{team_b}): ").strip()
        if resp.lower() in (team_a.lower(), team_a):
            return team_a
        if resp.lower() in (team_b.lower(), team_b):
            return team_b
        print(f"Invalid input. Enter exactly '{team_a}' or '{team_b}'.")


def play_match(team_a, team_b):
    wins = {team_a: 0, team_b: 0}
    games = []

    for i in range(3):
        winner = get_game_winner(team_a, team_b, i)
        games.append(winner)
        wins[winner] += 1

        if wins[team_a] == 2 or wins[team_b] == 2:
            break

    match_winner = team_a if wins[team_a] > wins[team_b] else team_b
    return {
        'teams': (team_a, team_b),
        'games': games,
        'score': (wins[team_a], wins[team_b]),
        'winner': match_winner,
    }


def main():
    teams = get_team_names()
    schedule = list(combinations(teams, 2))
    print('\nTournament schedule (round robin):')
    for i, (a, b) in enumerate(schedule, start=1):
        print(f"  {i}. {a} vs {b}")

    results = []
    standings = {team: {'match_wins': 0, 'match_losses': 0, 'games_won': 0, 'games_lost': 0} for team in teams}

    print('\nEnter match results (best of 3):')
    for a, b in schedule:
        print('\nMatch:', a, 'vs', b)
        match = play_match(a, b)
        results.append(match)

        a_wins, b_wins = match['score']
        standings[a]['games_won'] += a_wins
        standings[a]['games_lost'] += b_wins
        standings[b]['games_won'] += b_wins
        standings[b]['games_lost'] += a_wins

        winner = match['winner']
        loser = b if winner == a else a
        standings[winner]['match_wins'] += 1
        standings[loser]['match_losses'] += 1

    print('\nMatch results:')
    for match in results:
        a, b = match['teams']
        a_score, b_score = match['score']
        print(f"{a} {a_score} - {b_score} {b} | winner: {match['winner']} | games: {', '.join(match['games'])}")

    print('\nStandings:')
    ranked = sorted(standings.items(), key=lambda kv: (-kv[1]['match_wins'], -(kv[1]['games_won'] - kv[1]['games_lost'])))
    print(f"{'Team':<10} {'MW':>2} {'ML':>2} {'GW':>3} {'GL':>3} {'GD':>3}")
    for team, st in ranked:
        gd = st['games_won'] - st['games_lost']
        print(f"{team:<10} {st['match_wins']:>2} {st['match_losses']:>2} {st['games_won']:>3} {st['games_lost']:>3} {gd:>3}")

    top = ranked[0][0]
    print('\nChampion:', top)


if __name__ == '__main__':
    main()
