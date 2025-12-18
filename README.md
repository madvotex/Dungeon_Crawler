# 🕹️ Dungeon Crawler (Python + Pygame)

A procedural roguelike dungeon crawler built using **Python** and **Pygame**.  
Explore large randomly generated dungeons, avoid enemies, and progress through floors.

---

## 🎮 Game Features
- Large procedurally generated dungeon (rooms + corridors)
- Fog of war with light radius
- Minimap for explored areas
- Enemy AI with:
  - Line-of-sight (cannot see through walls)
  - Delayed chase behavior
  - Reduced movement speed
- Floor progression using stairs
- Difficulty scaling with floor number

---

## 🕹️ How to Play

### Controls
| Key | Action |
|----|-------|
| ↑ Arrow | Move Up |
| ↓ Arrow | Move Down |
| ← Arrow | Move Left |
| → Arrow | Move Right |
| Close Window | Exit Game |

---

### Objective
- Explore the dungeon
- Avoid enemies
- Find the **yellow stairs tile**
- Step on stairs to go to the **next floor**
- If an enemy touches you, the game **resets to Floor 1**

---

## ▶️ How to Run the Game

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/Dungeon-Crawler.git
cd Dungeon-Crawler
