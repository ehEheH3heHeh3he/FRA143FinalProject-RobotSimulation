from farm import Farm
from robot import PlanterRobot, WatererRobot
from task import Task


def main() -> None:
    # Minimum 10x5 grid with charging station C at (0, 0)
    farm = Farm(width=10, height=5, charger_pos=(0, 0))

    # At least 3 robots (R1 starts with low battery to showcase recharging)
    farm.add_robot(PlanterRobot(name="R1", pos=(0, 1), battery=25))
    farm.add_robot(PlanterRobot(name="R2", pos=(0, 2), battery=100))
    farm.add_robot(WatererRobot(name="R3", pos=(0, 3), battery=100))

    # At least 5 tasks (6 tasks total: 3 PLANT + 3 WATER)
    farm.add_task(Task(name="Plant Corn #1", task_type="PLANT", pos=(3, 1), duration=3))
    farm.add_task(Task(name="Plant Rice #2", task_type="PLANT", pos=(6, 2), duration=3))
    farm.add_task(Task(name="Plant Wheat #3", task_type="PLANT", pos=(8, 4), duration=2))
    farm.add_task(Task(name="Water Corn #1", task_type="WATER", pos=(4, 1), duration=2))
    farm.add_task(Task(name="Water Rice #2", task_type="WATER", pos=(7, 2), duration=2))
    farm.add_task(Task(name="Water Wheat #3", task_type="WATER", pos=(9, 4), duration=2))

    max_steps = 200
    while not farm.all_tasks_done() and farm.get_timestep() < max_steps:
        farm.step()

    farm.print_summary()


if __name__ == "__main__":
    main()