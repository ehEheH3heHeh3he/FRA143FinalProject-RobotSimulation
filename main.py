# main.py
from farm import Farm
from robot import PlanterRobot, WatererRobot
from task import Task

if __name__ == "__main__":
    farm = Farm(width=10, height=5)  # Minimum 10x5 grid[cite: 2]

    # At least 3 robots (can duplicate types)[cite: 2]
    farm.add_robot(PlanterRobot("R1", (0, 0)))
    farm.add_robot(PlanterRobot("R2", (0, 1)))
    farm.add_robot(WatererRobot("R3", (0, 2)))

    # At least 5 tasks[cite: 2]
    farm.add_task(Task("Plant Corn #1", "PLANT", (3, 1), duration=3))
    farm.add_task(Task("Plant Rice #2", "PLANT", (6, 2), duration=3))
    farm.add_task(Task("Plant Wheat #3", "PLANT", (8, 4), duration=2))
    farm.add_task(Task("Water Corn #1", "WATER", (4, 1), duration=2))
    farm.add_task(Task("Water Rice #2", "WATER", (7, 2), duration=2))

    while not farm.all_tasks_done():
        farm.step()
    # TODO: Print final summary (total timesteps & tasks per robot)[cite: 2]