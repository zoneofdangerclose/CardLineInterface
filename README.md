# Casino Card Games

A Python-based command-line casino game featuring Blackjack. Play classic casino Blackjack right in your terminal with persistent chip tracking across sessions.

## What is this?

This is a simple text-based casino game where you can play Blackjack against a dealer AI. Your chip count is saved between sessions, so you can build up your bankroll over time (or lose it all!).

## Getting Started

### What you need

- Python 3
- Two Python packages: `pandas` and `thefuzz`

### Installation

```bash
pip install pandas thefuzz
```

### Running the game

```bash
python CardLineInterface.py -g blackjack
```

## How to Play

You start with 100 chips. Each round you bet 10 chips trying to beat the dealer.

When it's your turn, type `y` to get another card or `n` to stick with what you have. The dealer plays automatically, and then you'll see who won!

## What's Included

- **Blackjack** - Fully playable
- **Poker** - Coming soon
- **Bank system** - Your chips are saved in a file called `bank.csv`
- **Game logs** - Each day's games are logged for debugging

## Example Gameplay

```
*♣♣♣♣ ♦♦♦♦ ♥♥♥♥ ♠♠♠♠*
Casino: Blackjack
Dealer hits on 15
*♣♣♣♣ ♦♦♦♦ ♥♥♥♥ ♠♠♠♠*

Dealers Hand:
['K♥', '??']

Your Hand:
['7♠', '9♦']

Chip Count
100
Bet
10
Hit? (y/n)
```

## Notes

- Currently only supports a single "guest" player
- Fixed betting amount (10 chips per round)
- Dealer follows Las Vegas rules (must hit on 15)
