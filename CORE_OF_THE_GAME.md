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
