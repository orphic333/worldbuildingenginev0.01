# The Core of the Game: What the Game is Actually About
> Date: 15/07/2026 | 
>> LLM's Utilised: GPT 5.5 (core discussion), Gemini Flash 3.5 (summary)
---
## Game Core Discussion
## 🎮 The Core Game Loop & Architecture

Your game is a high-stakes, macro-management dungeon simulator where growth and vulnerability are inexorably linked. The gameplay evokes the slow-burn, high-stress dread of *Plague Inc.* on Brutal difficulty, stretched over a long-form experience ("chess on a grand scale").

---

## 💎 The Resource & Growth Pipeline

The entire dungeon ecosystem is sustained by two foundational resources. Every other resource or mechanic in the game branches from this core:

| Resource | Nature | Acquisition | Purpose & Mechanics |
| --- | --- | --- | --- |
| **Aether** | Consumable & Cyclical | Generates naturally; must be manually mined. | Required to build dungeon levels, which spawn **Guardians**, who in turn use Aether to create **Units** (including **Builders**). |
| **Knowledge** | Permanent & Unlocking | Found as rare fragments in the outside world. | Deciphered to unlock new resources, expand strategic options, and allow the dungeon to grow. |

> ⚠️ **The Critical Aether Loop:** You need Builders to mine Aether. But if you run out of Aether, your Guardians cannot spawn Builders. If this chain breaks, your dungeon's growth completely halts.

---

## ☠️ Lose Conditions: The Twin Threats

1. **The Soft Bleed (Systemic Collapse):** Building yourself into an inescapable corner. If you mismanage your resources to the point where you cannot extract Aether or task builders, you are forced to helplessly watch your dungeon slowly stagnate and die.
2. **The Hard Wipe (Combat/Violence):**
* *External:* Organized human raiding parties invading your dungeon.
* *Internal:* **Rogue Guardians** rising up in rebellion due to poor management.



---

## 🧭 Outside Expeditions & Sentient Heroes

To obtain Knowledge, players must dispatch **Heroes** on surface-world expeditions.

### The Nature of Heroes

* They can live indefinitely but are permanent, high-value assets that are incredibly expensive to create.
* They possess the closest thing to **real sentience** in the game, granting them deep, emotional growth arcs.
* *The Tradeoff:* Their high sentience makes them highly effective, but also vulnerable to trauma, panic, or psychological collapse under high stress.

### The Expedition Interface

Expeditions are managed via a **semi-terminal command interface**. The player allocates a squad, chooses a destination, and sets the duration of the run (measured in *ticks*). Visually, the player monitors a live telemetry feed: a zoomed-out ASCII radar screen where heroes are represented by colored dots moving through a hostile environment.

The probability of finding Knowledge spikes in high-danger zones, forcing players to risk their prized, highly sentient heroes for survival-critical technological breakthroughs.

---

## 🕹️ The Interaction Dilemma: How Much Control?

We weighed three potential approaches for how the player interacts with expeditions while they are running:

* **Option A: Completely Hands-Off (Telemetry Only)**
* *How it works:* The player programs the expedition and watches it unfold purely as a spectator.
* *Pros:* Maximizes the tension and dread. Once they cross the threshold, you are powerless.
* *Cons:* Can feel deeply frustrating or unfair if a beloved, expensive hero dies to random bad luck (RNG).


* **Option B: Full Tactical Micro-Management**
* *How it works:* The player manually steers the ASCII dots, dodging enemies and directing combat.
* *Pros:* High player agency; skilled players can save their heroes from bad situations.
* *Cons:* Drastically disrupts the macro-management flow. It pauses the core dungeon-building gameplay to focus on tedious micro-management.

* **Option C: High-Level Delayed Directives (The Middle Ground)**
* *How it works:* The player cannot control step-by-step movement, but can transmit high-level terminal protocols (e.g., `PROTOCOL: STEALTH`, `PROTOCOL: SPEED_RUN`, or `ABORT_MISSION`). Because of the physical distance, these commands take a few ticks to actually reach the heroes.
* *Pros:* Preserves the "desperate bunker operator" terminal atmosphere, grants player agency to react to disasters, but keeps the focus entirely on high-level strategic decision-making.

# Initial Gamestate Discussion
> Date: 16/07/2026
> Gemini 3.5 Flash
## 📦 The Starting Setup: Levels, Guardians, and Units

The game begins with a strictly calibrated, high-scarcity scenario designed to instantly immerse the player in the core tension of the game:

* **Dungeon Layout:** The dungeon starts with **3 levels**.
* **The Guardians:** **3 Guardians** are present at start (1 on each level), each specialized in spawning a single type of unit:
* *Guardian 1:* Spawns **Heroes** (sentient, elite surface explorers).
* *Guardian 2:* Spawns **Builders** (the backbone of the dungeon economy).
* *Guardian 3:* Spawns **Warders** (the defenders of the dungeon).


* **The Initial Units:** The player is granted exactly enough resources to spawn a starting force of **1 Hero, 5 Builders, and 5 Warders**.

---

## 🧪 The Starting Resource Bank

To create these units, the player utilizes four core resources. Every recipe is bound together by **Aether Crystals**, which acts as the universal catalyst.

| Resource | Role & Thematic Justification |
| --- | --- |
| **Aether Crystals** | The universal magical binder required for all unit-creation recipes. |
| **Blood** | Biological sustenance used to spawn martial and sentient units (Warders and Heroes). |
| **Water** | The physical survival timer/fuel strictly used for the Hero's surface-world expeditions. |
| **Wood** *(or Subterranean Fungi/Scrap)* | Physical material used for crafting industrial units (Builders) and outfitting explorers (Heroes). |

### Recipe & Starting Stockpile Math:

To ensure the player spawns exactly their starting units and is left with an empty inventory, the recipes and starting bank are balanced as follows:

* **Builder Recipe:** $1\text{ Aether} + 1\text{ Wood}$ (Creates 5 $\rightarrow$ Costs **$5\text{ Aether}, 5\text{ Wood}$**)
* **Warder Recipe:** $1\text{ Aether} + 1\text{ Blood}$ (Creates 5 $\rightarrow$ Costs **$5\text{ Aether}, 5\text{ Blood}$**)
* **Hero Recipe:** $5\text{ Aether} + 2\text{ Blood} + 3\text{ Water} + 3\text{ Wood}$ (Creates 1 $\rightarrow$ Costs **$5\text{ Aether}, 2\text{ Blood}, 3\text{ Water}, 3\text{ Wood}$**)

> **Starting Player Stockpile:** $15\text{ Aether}$, $7\text{ Blood}$, $8\text{ Wood}$, and $3\text{ Water}$.
> Spawning the starting units consumes this stockpile to exactly **0**.

---

## 🧠 Design Rationales & Strategic Decisions

* **Instant Engagement (The "Zero-Waste" Principle):** Because spawning the starting units completely drains the player's initial stockpile, they cannot sit idle. On tick one, they are immediately forced to interact with the core loop: tasking their 5 Builders to mine Aether and preparing their 1 Hero for a surface expedition.
* **Thematic Plausibility of Wood:** To keep the subterranean theme intact, "Wood" is conceptualized as hard underground lichen-stalks, fossilized fungus, or salvaged scrap, preventing players from wondering how trees are growing in a deep dungeon.
* **Preventing the Chicken-and-Egg Blood Trap:** Because Blood is required for Warders, but Warders are needed to kill humans to harvest Blood, the Guardians do not demand immediate upkeep. They start in a **"sated" or "dormant"** state, giving the player a grace period of ticks to establish their economy before internal maintenance costs kick in.
* **Water Isolation:** Water is treated strictly as an expedition consumable rather than a dungeon-wide resource to prevent complex, early-game logistical bottlenecks like plumbing or well-management.