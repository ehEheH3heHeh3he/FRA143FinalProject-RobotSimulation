from robot import Robot
from task import Task


class Farm:
    def __init__(self, width: int = 10, height: int = 5, charger_pos: tuple[int, int] = (0, 0)):
        if width < 10 or height < 5:
            raise ValueError("Grid size must be at least 10x5.")
        # Composition: Farm owns the grid, charger, robots, and tasks
        self.__width = width
        self.__height = height
        self.__charger_pos = charger_pos
        self.__robots: list[Robot] = []
        self.__tasks: list[Task] = []
        self.__timestep = 0

    def get_width(self) -> int:
        return self.__width

    def get_height(self) -> int:
        return self.__height

    def get_charger_pos(self) -> tuple[int, int]:
        return self.__charger_pos

    def get_timestep(self) -> int:
        return self.__timestep

    def add_robot(self, robot: Robot) -> None:
        self.__robots.append(robot)

    def add_task(self, task: Task) -> None:
        self.__tasks.append(task)

    def step(self) -> None:
        """Advance simulation by 1 discrete timestep."""
        self.__timestep += 1

        # 1. Assign IDLE robots to charger (if battery low) or matching WAITING task
        for robot in self.__robots:
            if robot.get_status() == "IDLE":
                if robot.needs_charge():
                    robot.send_to_charger(self.__charger_pos)
                else:
                    for task in self.__tasks:
                        if task.get_status() == "WAITING" and robot.can_handle(task.get_type()):
                            robot.assign_task(task)
                            break

        # 2. Polymorphism: call work() on all robots in a single list
        for robot in self.__robots:
            robot.work()

        # 3. Render grid and status tables
        self.display_grid()

    def all_tasks_done(self) -> bool:
        return all(task.get_status() == "DONE" for task in self.__tasks)

    def display_grid(self) -> None:
        """Print the 2D grid, robot status table, and task counts."""
        print(f"\n=== Step {self.__timestep} ===")

        grid = [["." for _ in range(self.__width)] for _ in range(self.__height)]

        # Place charging station 'C'
        cx, cy = self.__charger_pos
        if 0 <= cx < self.__width and 0 <= cy < self.__height:
            grid[cy][cx] = "C"

        # Place unfinished tasks '*'
        for task in self.__tasks:
            if task.get_status() != "DONE":
                tx, ty = task.get_position()
                if 0 <= tx < self.__width and 0 <= ty < self.__height:
                    grid[ty][tx] = "*"

        # Place robots on top (e.g., "R1" -> "1")
        for robot in self.__robots:
            rx, ry = robot.get_position()
            if 0 <= rx < self.__width and 0 <= ry < self.__height:
                marker = robot.get_name()[-1] if robot.get_name() else "R"
                grid[ry][rx] = marker

        # Print column headers and rows
        print("  " + " ".join(str(x) for x in range(self.__width)))
        for y, row in enumerate(grid):
            print(f"{y} " + " ".join(row))

        # Print robot status table
        print("\nRobot | Type         | Pos    | Status   | Task            | Progress | Battery")
        print("-" * 82)
        for robot in self.__robots:
            task = robot.get_current_task()
            if task is not None:
                task_name = task.get_name()
                progress = f"{task.get_progress()}/{task.get_duration()}"
            else:
                task_name = "Charger (C)" if robot.get_status() == "CHARGING" else "-"
                progress = "-"

            robot_type = type(robot).__name__
            print(
                f"{robot.get_name():<5} | "
                f"{robot_type:<12} | "
                f"{str(robot.get_position()):<6} | "
                f"{robot.get_status():<8} | "
                f"{task_name:<15} | "
                f"{progress:<8} | "
                f"{robot.get_battery()}%"
            )

        # Print task summary counts
        waiting = sum(1 for t in self.__tasks if t.get_status() == "WAITING")
        in_progress = sum(1 for t in self.__tasks if t.get_status() == "IN_PROGRESS")
        done = sum(1 for t in self.__tasks if t.get_status() == "DONE")
        print(f"\nTasks: waiting {waiting} | in progress {in_progress} | done {done}")

    def print_summary(self) -> None:
        """Print final simulation statistics after all tasks finish."""
        print("\n=== Simulation Complete ===")
        print(f"Total timesteps used: {self.__timestep}")
        for robot in self.__robots:
            print(
                f"- {robot.get_name()} ({type(robot).__name__}): "
                f"{robot.get_tasks_completed()} tasks completed "
                f"(Battery remaining: {robot.get_battery()}%)"
            )