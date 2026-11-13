# This repository is for FRA143 Project which is a robot simulation 
This project is in development by Thanakrit Kulrattanarak and Jirat Sinchuen for FRA143 class.
The requirement of this project can be seen in file [Final_Project_Robot_Simulation](Final_Project_Robot_Simulation.pdf)\
The scenario for the robot work is it's in a farm

## Class Diagram
```mermaid
classDiagram
    class Farm {
        -int width
        -int height
        -list~Robot~ robots
        -list~Task~ tasks
        -int timestep
        +__init__(width: int, height: int)
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
        +__init__(name: str, pos: tuple, battery: int)
        +__del__() void
        +get_name() str
        +get_position() tuple~int,int~
        +get_battery() int
        +get_status() str
        +get_current_task() Task
        +get_tasks_completed() int
        +consume_battery(amount: int) void
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