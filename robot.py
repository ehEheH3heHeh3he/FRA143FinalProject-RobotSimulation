from abc import ABC, abstractmethod
from task import Task


class Robot(ABC):
    def __init__(self, name: str, pos: tuple[int, int], battery: int = 100):
        # Constructor & Encapsulation
        self.__name = name
        self.__pos = pos
        self.__battery = max(0, min(100, battery))
        self.__status = "IDLE"  # IDLE, MOVING, WORKING, CHARGING
        self.__current_task: Task | None = None
        self.__tasks_completed = 0
        self.__charger_pos: tuple[int, int] | None = None

    def __del__(self):
        # Destructor: clean up object references
        self.__current_task = None
        self.__charger_pos = None

    # --- Encapsulated Getters ---
    def get_name(self) -> str:
        return self.__name

    def get_position(self) -> tuple[int, int]:
        return self.__pos

    def get_battery(self) -> int:
        return self.__battery

    def get_status(self) -> str:
        return self.__status

    def get_current_task(self) -> Task | None:
        return self.__current_task

    def get_tasks_completed(self) -> int:
        return self.__tasks_completed

    # --- Protected State Helper for Subclasses ---
    def _set_status(self, status: str) -> None:
        self.__status = status

    # --- Encapsulated Battery & Recharging Methods ---
    def consume_battery(self, amount: int) -> None:
        """Reduce battery safely without dropping below 0."""
        self.__battery = max(0, self.__battery - amount)

    def recharge(self, amount: int = 25) -> None:
        """Increase battery safely without exceeding 100."""
        self.__battery = min(100, self.__battery + amount)

    def needs_charge(self, threshold: int = 25) -> bool:
        return self.__battery <= threshold

    def send_to_charger(self, charger_pos: tuple[int, int]) -> None:
        self.__charger_pos = charger_pos
        self.__status = "CHARGING"

    def handle_charging(self) -> bool:
        """
        Handle movement toward the charging station and recharging.
        Returns True if this timestep was spent charging/moving to charger.
        """
        if self.__status != "CHARGING" or self.__charger_pos is None:
            return False

        if self.__pos != self.__charger_pos:
            self.move_one_step_toward(self.__charger_pos)
        else:
            self.recharge(25)
            if self.__battery >= 100:
                self.__charger_pos = None
                self.__status = "IDLE"
        return True

    # --- Movement & Task Lifecycle ---
    def move_one_step_toward(self, target: tuple[int, int]) -> None:
        """Move 1 tile per timestep (horizontal first, then vertical)."""
        if self.__battery <= 0:
            return

        x, y = self.__pos
        tx, ty = target
        if x < tx:
            self.__pos = (x + 1, y)
        elif x > tx:
            self.__pos = (x - 1, y)
        elif y < ty:
            self.__pos = (x, y + 1)
        elif y > ty:
            self.__pos = (x, y - 1)

        if (x, y) != self.__pos:
            self.consume_battery(1)

    def assign_task(self, task: Task) -> None:
        self.__current_task = task
        task.set_status("IN_PROGRESS")
        if self.__pos == task.get_position():
            self.__status = "WORKING"
        else:
            self.__status = "MOVING"

    def complete_current_task(self) -> None:
        self.__current_task = None
        self.__status = "IDLE"
        self.__tasks_completed += 1

    # --- Polymorphic Interface ---
    @abstractmethod
    def can_handle(self, task_type: str) -> bool:
        pass

    @abstractmethod
    def work(self) -> None:
        pass


class PlanterRobot(Robot):
    """Subclass specialized in PLANT tasks."""

    def can_handle(self, task_type: str) -> bool:
        return task_type == "PLANT"

    def work(self) -> None:
        if self.handle_charging():
            return

        task = self.get_current_task()
        if task is None:
            return

        target = task.get_position()
        if self.get_position() != target:
            self.move_one_step_toward(target)
            if self.get_position() == target:
                self._set_status("WORKING")
        else:
            self._set_status("WORKING")
            self.consume_battery(2)
            if task.advance_progress():
                self.complete_current_task()


class WatererRobot(Robot):
    """Subclass specialized in WATER tasks."""

    def can_handle(self, task_type: str) -> bool:
        return task_type == "WATER"

    def work(self) -> None:
        if self.handle_charging():
            return

        task = self.get_current_task()
        if task is None:
            return

        target = task.get_position()
        if self.get_position() != target:
            self.move_one_step_toward(target)
            if self.get_position() == target:
                self._set_status("WORKING")
        else:
            self._set_status("WORKING")
            self.consume_battery(1)
            if task.advance_progress():
                self.complete_current_task()