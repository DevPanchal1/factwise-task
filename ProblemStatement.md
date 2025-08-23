# Team Project Planner - TaskWIse Task

## Overview

This project is a **lightweight project planner tool** designed to help teams manage project boards and tasks.  
It provides simple APIs that work with JSON strings for both input and output, while using local file storage for persistence.  

Think of it as a minimal Trello-like backend that focuses more on the fundamentals of project and team management rather than UI.  

---

## Thought Process

While designing this project, the main goals were **clarity, simplicity, and extensibility**:

1. **Abstractions** – Base classes were introduced for boards, teams, and users so that future extensions (e.g., DB integrations, new APIs) can be plugged in easily.  
2. **Persistence** – Chose JSON files for storage because they’re human-readable, easy to debug, and perfect for prototyping.  
3. **Modularity** – Code is separated into base classes and concrete implementations to keep things clean.  
4. **Error Handling** – Added meaningful exceptions so developers can understand what went wrong without digging through stack traces.  

---

## Assumptions

To keep the design lean, a few assumptions were made:

1. **Input format** – Board, task, and user data are always supplied as valid JSON strings.  
2. **Identifiers** – IDs for boards, tasks, and users are assumed to be unique and are provided by the caller (no auto-generation for now).  

---

## Usage

1. Define your board, team, and user implementations by extending the base classes:
   - `project_board_base.py`  
   - `team_base.py`  
   - `user_base.py`  
2. Interact with the planner APIs by sending/receiving JSON strings.  
3. Data is stored locally, so you can inspect and tweak it easily if needed.  

---