# PoE 2 Auto Crafter (v1.31)

A Chaos/Alteration Spam crafting tool designed for **Path of Exile 2**, built with Python. Focused on speed, precision, and stability.

![PoE2 Crafter](https://img.shields.io/badge/Status-Stable-green) ![Platform](https://img.shields.io/badge/Platform-Windows-blue)

## ✨ What's New in v1.31 (Regex & Parsing Overhaul)

* **🧹 Ultimate Bracket Cleaner:** The bot now automatically strips all brackets `(...)` and `{...}` from both the game's clipboard and your input text. It flawlessly handles PoE2's Advanced Mod descriptions and trade site formats.
* **🎯 True Minimum Value Targeting:** Set your exact minimum required roll (e.g., `47 to Spirit`), and the bot will stop only when it hits that number or higher.
* **🛡️ Smart Filtering:** Automatically ignores **Fractured**, **Implicit**, and flavor texts. It only checks for *new* rolls.
* **⚡ Stable Logic:** Uses a **Continuous Shift-Hold** method with optimized timing to ensure smooth operation without missing inputs. Works beautifully with extremely fast currencies like Orbs of Alteration.
* **🛑 Emergency Stop:** Stop operations immediately by pressing the **`X`** key.

## 📥 Installation

1.  Go to the **[Releases](../../releases)** page of this repository.
2.  Download the latest **`poe_crafter.exe`** file.
3.  Place the file anywhere on your computer (No Python installation required).

## 🚀 How to use

**⚠️ IMPORTANT:** Always right-click the program and select **"Run as administrator"** (Required for mouse/keyboard control).

1.  **Prepare Mods:**
    * Type or paste your desired mods into the text box.
    * *See the "Input Rules" section below for the best results.*

2.  **Set Coordinates:**
    * Click **`1. Set Chaos/Alt`** -> Hover your mouse over the Currency stack (Chaos Orb, Orb of Alteration, etc.) in-game (**Wait 2 seconds**).
    * Click **`2. Set Item`** -> Hover your mouse over the item you want to craft (**Wait 2 seconds**).

3.  **Start Crafting:**
    * Click the **`START CRAFTING`** button and release your mouse/keyboard.

4.  **Stopping:**
    * Press the **`X`** key on your keyboard to stop immediately.

## 📝 Input Rules & Examples (Crucial for v1.31)

Thanks to the new auto-cleaner, you need to structure your inputs based on what you want to achieve:

**🎯 Goal 1: I want a specific Minimum Value (Recommended)**
Do not include `(x-y)` ranges. Just type the minimum number you accept + the text.
```text
47 to Spirit
92% increased Energy Shield
allow rerolling Favours 3
