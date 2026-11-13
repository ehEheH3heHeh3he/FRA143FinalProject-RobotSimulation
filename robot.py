from abc import ABC, abstractmethod
from task import Task

class Robot(ABC):
    def __init__(self, name: str, pos: tuple[int, int], battery: int = 100):
        # Constructor & Encapsulation[cite: 2, 3]
        self.__name = name
        self.__pos = pos
        self.__battery = battery
        self.__status = "IDLE"            # IDLE, MOVING, WORKING[cite: 2]
        self.__current_task: Task | None = None
        self.__tasks_completed = 0

    def __del__(self):
        # Destructor requirement[cite: 3]
        pass

    # --- Controlled Getters & Setters (Encapsulation)[cite: 2] ---
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

    def consume_battery(self, amount: int) -> None:
        # Battery cannot drop below 0[cite: 2]
        self.__battery = max(0, self.__battery - amount)

    def move_one_step_toward(self, target: tuple[int, int]) -> None:
        """Move 1 tile per timestep (horizontal first, then vertical)[cite: 2]."""
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
        self.consume_battery(1)

    def assign_task(self, task: Task) -> None:
        self.__current_task = task
        self.__status = "MOVING"
        task.set_status("IN_PROGRESS")

    def complete_current_task(self) -> None:
        self.__current_task = None
        self.__status = "IDLE"
        self.__tasks_completed += 1
    def recharge(self, amount: int = 25) -> None:
        # Encapsulation: battery cannot exceed 100
        self.__battery = min(100, self.__battery + amount)

    def needs_charging(self, threshold: int = 25) -> bool:
        return self.__battery <= threshold or self.__status == "CHARGING"

    def handle_charging(self, charger_pos: tuple[int, int]) -> None:
        self._set_status("CHARGING")
        if self.get_position() != charger_pos:
            self.move_one_step_toward(charger_pos)
            # Refund the 1% movement cost so a low-battery robot never strands at 0%
            self.recharge(1)
        else:
            self.recharge(25)
            if self.get_battery() >= 100:
                self._set_status("MOVING" if self.get_current_task() else "IDLE")

    @abstractmethod
    def can_handle(self, task_type: str) -> bool:
        """Return True only if this subclass handles task_type[cite: 2]."""
        pass

    @abstractmethod
    def work(self) -> None:
        """Polymorphic action called every timestep without if-type checks[cite: 2]."""
        pass


# --- Inheritance: 2 Subclasses for a Group of 2[cite: 2, 3] ---
class PlanterRobot(Robot):
    def can_handle(self, task_type: str) -> bool:
        return task_type == "PLANT"

    def work(self) -> None:
        # TODO: If MOVING toward task, move 1 step; once at task pos, advance_progress()[cite: 2]
        pass


class WatererRobot(Robot):
    def can_handle(self, task_type: str) -> bool:
        return task_type == "WATER"

    def work(self) -> None:
        # TODO: If MOVING toward task, move 1 step; once at task pos, advance_progress()[cite: 2]
        pass