# PoE 2 Auto Crafter (v1.30)

A Chaos Spam crafting tool designed for **Path of Exile 2**, built with Python. Focused on speed, precision, and stability.

![PoE2 Crafter](https://img.shields.io/badge/Status-Stable-green) ![Platform](https://img.shields.io/badge/Platform-Windows-blue)

## ✨ Features in v1.30

* **🛡️ Smart Filtering:** Automatically ignores **Fractured** and **Implicit** mods. The bot will no longer stop prematurely on existing mods; it only checks for *new* rolls.
* **⚡ Stable Logic:** Uses a **Continuous Shift-Hold** method with optimized timing (0.08s) to ensure smooth operation without missing inputs.
* **abc Text Mod Support:** Now supports **Text-Only** mods (e.g., *"Upgrades Radius to Large"*) in addition to numerical values.
* **Smart Parsing:** Supports copying Mod text directly from **[poe2db.tw](https://poe2db.tw/)** (Handles all dash types: -, –, —).
* **Emergency Stop:** Stop operations immediately by pressing the **`X`** key.

## 📥 Installation

1.  Go to the **[Releases](../../releases)** page of this repository.
2.  Download the latest **`poe_crafter.exe`** file.
3.  Place the file anywhere on your computer (No Python installation required).

## 🚀 How to use

**⚠️ IMPORTANT:** Always right-click the program and select **"Run as administrator"** (Required for mouse/keyboard control).

1.  **Prepare Mods:**
    * Go to [poe2db](https://poe2db.tw/), copy the desired mods, and paste them into the program.
    * *Tip: You can mix number mods and text mods.*

2.  **Set Coordinates:**
    * Click **`1. Set Chaos`** -> Hover your mouse over the Chaos Orb stack in-game (**Wait 2 seconds**).
    * Click **`2. Set Item`** -> Hover your mouse over the item you want to craft (**Wait 2 seconds**).

3.  **Start Crafting:**
    * Click the **`START CRAFTING`** button and release your mouse/keyboard.

4.  **Stopping:**
    * Press the **`X`** key on your keyboard to stop immediately.

### Input Example

You can paste data like this directly into the program (Supports both numbers and text):

```text
Adds (20–30) to (40–50) Physical Damage
(170–179)% increased Physical Damage
Upgrades Radius to Large
