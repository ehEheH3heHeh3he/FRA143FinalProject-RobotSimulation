class Task:
    def init(self, name: str, task_type: str, pos: tuple[int, int], duration: int):
        if duration <= 0:
            raise ValueError("Task duration must be at least 1 timestep.")
        # Encapsulation: private attributes
        self.name = name
        self.task_type = task_type
        self.pos = pos
        self.duration = duration
        self.progress = 0
        self.status = "WAITING"  # WAITING, IN_PROGRESS, DONE

    def get_name(self) -> str:
        return self.name

    def get_type(self) -> str:
        return self.task_type

    def get_position(self) -> tuple[int, int]:
        return self.pos

    def get_duration(self) -> int:
        return self.duration

    def get_progress(self) -> int:
        return self.progress

    def get_status(self) -> str:
        return self.status

    def set_status(self, status: str) -> None:
        if status not in ("WAITING", "IN_PROGRESS", "DONE"):
            raise ValueError(f"Invalid task status: {status}")
        self.status = status

    def advance_progress(self) -> bool:
        """Advance task progress by 1 timestep. Returns True when completed."""
        if self.status == "DONE":
            return True
        self.progress += 1
        if self.progress >= self.duration:
            self.status = "DONE"
            return True
        return False