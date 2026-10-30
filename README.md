# turn-based-rpg
A self directed Python project to explore OOP and game making.

# Turn Based Combat Game
A self directed Python project made to explore object-oriented programming and probabilistic game logic.

## About the Project
This is a text based combat simulator. I've always been interested in RPG combat games, and in my first month of university, python class taught me OOP. I got the idea to make this fun project to apply what i know about classes and managing game states. It features four playable classes right now (Mage, Archer, Knight, Assassin) each with their own unique abilities, resource system, stats, and a combat engine that does damage calculation, dodges, critical hits, and status effects. 

## How to Run
1. Have python installed
2. Download or clone this repo
3. Run `first.py` in your terminal: `python first.py`

## What I learned from this project
- Designing a class hierarchy with inheritance and polymorphism
- Implementing finite state machines for cooldowns and buffs/debuffs.
- Using `random` to reduce monotonicity in combat.
- Debugging logical errors in turn order and state transitions.

## Future Improvements
This project is far from done and I am not satisfied yet, I am planning to:
1. Alter the turn system rather than make player 1 always move before player 2.
2. Adding more unique classes, I am thinking of adding a summoner which can summon a separate entity that we can command. That would of course be more complicated and would probably require changing the game system.
3. Adding the ability to pick weapons rather than leaving it up to luck. Also will change weapon system to provide unique effects instead of extra damage to make the game more skill based rather than luck.
4. Implement a GUI.
5. Refactor the damage calculation pipeline for better extensibility.
6. Work on balancing the classes, stats, and weapons.
