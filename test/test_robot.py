import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from farm import Farm
from robot import PlanterRobot, WatererRobot
from task import Task


# --- 1. Core Robot Attributes, Movement & Encapsulation Tests ---

def test_robot_initial_attributes():
    robot = PlanterRobot("R1", (1, 2), battery=100)
    assert robot.get_name() == "R1"
    assert robot.get_position() == (1, 2)
    assert robot.get_battery() == 100
    assert robot.get_status() == "IDLE"
    assert robot.get_current_task() is None
    assert robot.get_tasks_completed() == 0


def test_battery_cannot_drop_below_zero():
    robot = PlanterRobot("R1", (0, 0), battery=10)
    robot.consume_battery(25)
    assert robot.get_battery() == 0


def test_move_one_step_horizontal_first():
    robot = PlanterRobot("R1", (0, 0), battery=100)
    robot.move_one_step_toward((2, 2))
    assert robot.get_position() == (1, 0)
    assert robot.get_battery() == 99


def test_robot_task_type_matching():
    planter = PlanterRobot("R1", (0, 0))
    waterer = WatererRobot("R2", (0, 1))

    assert planter.can_handle("PLANT") is True
    assert planter.can_handle("WATER") is False
    assert waterer.can_handle("WATER") is True
    assert waterer.can_handle("PLANT") is False


def test_polymorphic_work_execution():
    planter = PlanterRobot("R1", (0, 0), battery=100)
    waterer = WatererRobot("R2", (0, 0), battery=100)

    plant_task = Task("Plant Corn", "PLANT", (0, 0), duration=1)
    water_task = Task("Water Corn", "WATER", (0, 0), duration=1)

    planter.assign_task(plant_task)
    waterer.assign_task(water_task)

    robots = [planter, waterer]
    for robot in robots:
        robot.work()

    assert plant_task.get_status() == "DONE"
    assert water_task.get_status() == "DONE"
    assert planter.get_battery() == 98  # Planter uses 2 battery per work step
    assert waterer.get_battery() == 99  # Waterer uses 1 battery per work step


# --- 2. Extra Feature: Recharging & Charging Station Tests ---

def test_recharge_caps_at_100():
    robot = PlanterRobot("R1", (0, 0), battery=90)
    robot.recharge(25)
    assert robot.get_battery() == 100


def test_low_battery_robot_goes_to_charger_instead_of_task():
    farm = Farm(width=10, height=5, charger_pos=(0, 0))
    robot = PlanterRobot("R1", (2, 0), battery=20)
    task = Task("Plant Corn", "PLANT", (5, 0), duration=2)

    farm.add_robot(robot)
    farm.add_task(task)
    farm.step()

    assert robot.get_status() == "CHARGING"
    assert robot.get_position() == (1, 0)
    assert robot.get_battery() == 19
    assert task.get_status() == "WAITING"


def test_robot_returns_to_idle_when_fully_charged():
    farm = Farm(width=10, height=5, charger_pos=(0, 0))
    robot = PlanterRobot("R1", (0, 0), battery=20)
    farm.add_robot(robot)

    # 4 steps at +25 per step: 20 -> 45 -> 70 -> 95 -> 100
    for _ in range(4):
        farm.step()

    assert robot.get_battery() == 100
    assert robot.get_status() == "IDLE"