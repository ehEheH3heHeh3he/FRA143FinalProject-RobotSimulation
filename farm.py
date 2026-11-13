# farm.py
from robot import Robot
from task import Task


class Farm:
    def __init__(self, width: int = 10, height: int = 5, charger_pos: tuple[int, int] = (0, 0)):
        # Composition: Farm owns the grid dimensions, charger, robots, and tasks
        self.__width = width
        self.__height = height
        self.__charger_pos = charger_pos
        self.__robots: list[Robot] = []
        self.__tasks: list[Task] = []
        self.__timestep = 0

    def get_charger_pos(self) -> tuple[int, int]:
        return self.__charger_pos

    def add_robot(self, robot: Robot) -> None:
        self.__robots.append(robot)

    def add_task(self, task: Task) -> None:
        self.__tasks.append(task)

    def step(self) -> None:
        """Advance simulation by 1 discrete timestep[cite: 2]."""
        self.__timestep += 1

        # 1. For IDLE robots: prioritize low-battery charging before assigning new tasks[cite: 2, 3]
        for robot in self.__robots:
            if robot.get_status() == "IDLE":
                if robot.needs_charge():
                    robot.send_to_charger(self.__charger_pos)
                else:
                    for task in self.__tasks:
                        if task.get_status() == "WAITING" and robot.can_handle(task.get_type()):
                            robot.assign_task(task)
                            break

        # 2. Polymorphism: call work() on every robot without checking robot type[cite: 2]
        for robot in self.__robots:
            robot.work()

        # 3. Render the 2D grid and status tables every timestep[cite: 2]
        self.display_grid()

    def all_tasks_done(self) -> bool:
        return all(task.get_status() == "DONE" for task in self.__tasks)

    def display_grid(self) -> None:
        """Display the 2D grid, robot status table, and task counts on the terminal[cite: 2]."""
        print(f"\n=== Step {self.__timestep} ===")

        # Build empty grid filled with '.'
        grid = [["." for _ in range(self.__width)] for _ in range(self.__height)]

        # Place charging station 'C'[cite: 1]
        cx, cy = self.__charger_pos
        if 0 <= cx < self.__width and 0 <= cy < self.__height:
            grid[cy][cx] = "C"

        # Place active tasks '*'[cite: 1]
        for task in self.__tasks:
            if task.get_status() != "DONE":
                tx, ty = task.get_position()
                if 0 <= tx < self.__width and 0 <= ty < self.__height:
                    grid[ty][tx] = "*"

        # Place robots on top (e.g., "R1" -> "1" so grid columns stay aligned)[cite: 2]
        for robot in self.__robots:
            rx, ry = robot.get_position()
            if 0 <= rx < self.__width and 0 <= ry < self.__height:
                marker = robot.get_name()[-1] if robot.get_name() else "R"
                grid[ry][rx] = marker

        # Print column headers and rows[cite: 2]
        header = "  " + " ".join(str(x) for x in range(self.__width))
        print(header)
        for y, row in enumerate(grid):
            print(f"{y} " + " ".join(row))

        # Print robot status table[cite: 2]
        print("\nRobot | Type         | Pos    | Status   | Task           | Battery")
        print("-" * 70)
        for robot in self.__robots:
            task = robot.get_current_task()
            task_name = task.get_name() if task else "-"
            robot_type = type(robot).__name__
            print(
                f"{robot.get_name():<5} | "
                f"{robot_type:<12} | "
                f"{str(robot.get_position()):<6} | "
                f"{robot.get_status():<8} | "
                f"{task_name:<14} | "
                f"{robot.get_battery()}%"
            )

        # Print task progress summary[cite: 2]
        waiting = sum(1 for t in self.__tasks if t.get_status() == "WAITING")
        in_progress = sum(1 for t in self.__tasks if t.get_status() == "IN_PROGRESS")
        done = sum(1 for t in self.__tasks if t.get_status() == "DONE")
        print(f"\nTasks: waiting {waiting} | in progress {in_progress} | done {done}")

    def print_summary(self) -> None:
        """Display final summary once all tasks are complete[cite: 2]."""
        print("\n=== Simulation Complete ===")
        print(f"Total timesteps used: {self.__timestep}")
        for robot in self.__robots:
            print(f"- {robot.get_name()} ({type(robot).__name__}): {robot.get_tasks_completed()} tasks completed")