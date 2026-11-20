class Task:
    def __init__(self, name: str, task_type: str, pos: tuple[int, int], duration: int):
        if duration <= 0:
            raise ValueError("Task duration must be at least 1 timestep.")
        # Encapsulation: private attributes
        self.__name = name
        self.__task_type = task_type
        self.__pos = pos
        self.__duration = duration
        self.__progress = 0
        self.__status = "WAITING"  # WAITING, IN_PROGRESS, DONE

    def get_name(self) -> str:
        return self.__name

    def get_type(self) -> str:
        return self.__task_type

    def get_position(self) -> tuple[int, int]:
        return self.__pos

    def get_duration(self) -> int:
        return self.__duration

    def get_progress(self) -> int:
        return self.__progress

    def get_status(self) -> str:
        return self.__status

    def set_status(self, status: str) -> None:
        if status not in ("WAITING", "IN_PROGRESS", "DONE"):
            raise ValueError(f"Invalid task status: {status}")
        self.__status = status

    def advance_progress(self) -> bool:
        """Advance task progress by 1 timestep. Returns True when completed."""
        if self.__status == "DONE":
            return True
        self.__progress += 1
        if self.__progress >= self.__duration:
            self.__status = "DONE"
            return True
        return False