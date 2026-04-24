<h1 align="center">
    <img src="assets/images/wK.png" width="28"> Ultimate Python Chess
</h1>

<p align="center">
    <i>A premium chess experience built with Python and Pygame, featuring a smart Minimax AI.</i>
</p>

<p align="center">
  <!-- Mandatory Badges -->
  <a href="#getting-started"><img src="https://img.shields.io/badge/Get%20Started-Click%20Here-brightgreen" alt="Get Started" /></a>
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License MIT" /> 
  <!-- Recommended Badges -->
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python Version" />
  <img src="https://img.shields.io/badge/Contributions-Welcome-orange" alt="Contributions Welcome" />
  <img src="https://img.shields.io/badge/Beginner%20Friendly-Yes-success" alt="Beginner Friendly" />
</p>

<p align="center">
  <img src="assets/images/board_preview.png" alt="ScreenCapture" width="400" >
</p>

## 📖 About

**Ultimate Python Chess** is a complete, feature-rich chess application designed to provide a premium playing experience. Whether you want to test your skills against a smart AI or play locally with a friend, this project offers a polished interface and robust implementation of all chess rules.

Built as part of a journey into game development and Artificial Intelligence, this project demonstrates core concepts like the **Minimax algorithm**, **Alpha-Beta pruning**, and object-oriented design in Python.

---

## ✨ Features

- **Intuitive GUI**: Sleek interface with smooth piece movement and real-time move highlighting.
- **Smart AI Opponent**: Challenge yourself with Easy, Medium, and Hard difficulty levels.
- **Advanced AI Logic**: Uses Minimax with Alpha-Beta pruning for efficient decision-making.
- **Full Ruleset**: Complete implementation of standard chess rules including:
    - Castling (Kingside and Queenside)
    - En Passant captures
    - Pawn Promotion (with piece selection)
    - Check, Checkmate, and Stalemate detection
- **Game History**: Real-time move log in algebraic notation.
- **Save & Load**: Save your games to resume them later.
- **Audio Feedback**: Immersive sound effects for moves, captures, and check alerts.

---

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.10 or higher
- [Pygame](https://www.pygame.org/news) library

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-username/Ultimate-Python-Chess.git
cd Ultimate-Python-Chess
```

2. **Install dependencies**

```bash
pip install pygame
```

3. **Run the game**

```bash
python main.py
```

---

## 📂 Project Structure

```
Ultimate-Python-Chess/
│
├── main.py           # Game entry point and event loop
├── game.py           # Core game state management
├── board.py          # Board representation and move validation
├── ai.py             # Minimax AI with Alpha-Beta pruning
├── pieces.py         # Definitions for all chess pieces
├── gui.py            # Pygame rendering and UI components
├── menu.py           # Game menu and difficulty selection
├── constants.py      # Global configuration and colors
├── utils.py          # Asset loading and helper functions
│
├── assets/           # Graphics (pieces, board) and sound effects
└── README.md
```

---

## 🛠️ Technologies Used

- **Python** – Core logic and AI
- **Pygame** – Graphics rendering, event handling, and audio
- **Pickle** – Game state serialization for saving/loading

---

## 📋 Requirements

```txt
pygame>=2.0.0
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🌟 Show Your Support

If you find this project helpful, please give it a ⭐️ on GitHub!

---

## 🤝 Contributing

Contributions are welcome! Whether it's fixing bugs, adding new features (like online multiplayer or engine integration), or improving the design, feel free to fork and submit a PR.

---

## 🗺️ Roadmap

- [x] Implement AI with Alpha-Beta pruning
- [x] Add Pawn Promotion UI
- [ ] Add Stockfish engine support
- [ ] Implement Online Multiplayer
- [ ] Add customizable board themes

---

<p align="center">
  Built with ❤️ by a Chess Enthusiast
</p>
