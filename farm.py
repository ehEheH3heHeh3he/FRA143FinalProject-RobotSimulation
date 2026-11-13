# farm.py
from robot import Robot
from task import Task

class Farm:
    def __init__(self, width: int = 10, height: int = 5):
        # Composition: Farm owns the grid, robots, and tasks[cite: 2]
        self.__width = width
        self.__height = height
        self.__robots: list[Robot] = []
        self.__tasks: list[Task] = []
        self.__timestep = 0

    def add_robot(self, robot: Robot) -> None:
        self.__robots.append(robot)

    def add_task(self, task: Task) -> None:
        self.__tasks.append(task)

    def step(self) -> None:
        """Run 1 discrete timestep: assign idle robots, call work(), display grid[cite: 2]."""
        self.__timestep += 1
        # 1. Assign WAITING tasks to matching IDLE robots[cite: 2]
        # 2. Polymorphism: loop over self.__robots and call robot.work()[cite: 2]
        # 3. Print ASCII grid and status table[cite: 2]

    def all_tasks_done(self) -> bool:
        return all(t.get_status() == "DONE" for t in self.__tasks)