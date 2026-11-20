# FRA143 Final Project: Farm Robot Simulation

A discrete-timestep 2D grid simulation of autonomous farming robots built with Object-Oriented Programming (OOP) in Python.

## Simulation Overview
- **Grid World:** $10 \times 5$ 2D farm grid containing a Solar Charging Station (`C`), active crop tasks (`*`), and autonomous robots (`1`, `2`, `3`).
- **Robots (2 Types):**
  - `PlanterRobot`: Moves to `PLANT` tasks and plants crops (consumes 2% battery per work step).
  - `WatererRobot`: Moves to `WATER` tasks and irrigates crops (consumes 1% battery per work step).
- **Extra Feature (Low-Battery Recharging):** When an idle robot's battery drops to `25%` or below, it prioritizes navigating to the Charging Station `C` at `(0, 0)` and recharges (`+25%` per timestep, capped at `100%`) before accepting new tasks.

## How to Run & Test
1. **Run the simulation:**
   ```bash
   main.py
   ```
2. **Run unit tests:**
   ```bash
   pytest
   ```

## Class Diagram
```mermaid
classDiagram
    class Farm {
        -int width
        -int height
        -tuple~int,int~ charger_pos
        -list~Robot~ robots
        -list~Task~ tasks
        -int timestep
        +__init__(width: int, height: int, charger_pos: tuple)
        +get_width() int
        +get_height() int
        +get_charger_pos() tuple~int,int~
        +get_timestep() int
        +add_robot(robot: Robot) void
        +add_task(task: Task) void
        +step() void
        +all_tasks_done() bool
        +display_grid() void
        +print_summary() void
    }

    class Robot {
        <<abstract>>
        -str name
        -tuple~int,int~ pos
        -int battery
        -str status
        -Task current_task
        -int tasks_completed
        -tuple~int,int~ charger_pos
        +__init__(name: str, pos: tuple, battery: int)
        +__del__() void
        +get_name() str
        +get_position() tuple~int,int~
        +get_battery() int
        +get_status() str
        +get_current_task() Task
        +get_tasks_completed() int
        +consume_battery(amount: int) void
        +recharge(amount: int) void
        +needs_charge(threshold: int) bool
        +send_to_charger(charger_pos: tuple) void
        +handle_charging() bool
        +move_one_step_toward(target: tuple) void
        +assign_task(task: Task) void
        +complete_current_task() void
        +can_handle(task_type: str)* bool
        +work()* void
    }

    class PlanterRobot {
        +can_handle(task_type: str) bool
        +work() void
    }

    class WatererRobot {
        +can_handle(task_type: str) bool
        +work() void
    }

    class Task {
        -str name
        -str task_type
        -tuple~int,int~ pos
        -int duration
        -int progress
        -str status
        +__init__(name: str, task_type: str, pos: tuple, duration: int)
        +get_name() str
        +get_type() str
        +get_position() tuple~int,int~
        +get_duration() int
        +get_progress() int
        +get_status() str
        +set_status(status: str) void
        +advance_progress() bool
    }

    Farm "1" *-- "3..*" Robot : manages
    Farm "1" *-- "5..*" Task : tracks
    Robot <|-- PlanterRobot : inherits
    Robot <|-- WatererRobot : inherits
    Robot "0..1" --> "0..1" Task : executes
```

## OOP Concepts in Code
| OOP Concept | Implementation Location |
| :--- | :--- |
| **Encapsulation** | Private attributes (`__battery`, `__pos`, `__status`, `__progress`) in `Robot`, `Task`, and `Farm` are modified only through validated methods such as `consume_battery()` (`>= 0`) and `recharge()` (`<= 100`). |
| **Inheritance** | `PlanterRobot` and `WatererRobot` inherit shared state, movement, and charging logic from the abstract base class `Robot`. |
| **Polymorphism** | `Farm.step()` iterates over a single `list[Robot]` and calls `robot.work()` on each instance without checking `type(robot)`. |
| **Composition** | `Farm` owns and coordinates collections of `Robot` and `Task` objects throughout the simulation lifecycle. |
| **Constructor & Destructor** | `__init__()` initializes valid object states across all classes, and `Robot.__del__()` releases task references upon cleanup. |