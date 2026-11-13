class Task:
    def init(self, name: str, task_type: str, pos: tuple[int, int], duration: int):
        # Encapsulation: keep attributes private with double underscores[cite: 2]
        self.name = name
        self.task_type = task_type      # e.g., "PLANT" or "WATER"[cite: 1, 3]
        self.pos = pos                  # (x, y) on the grid[cite: 2]
        self.duration = duration        # timesteps needed to finish[cite: 2]
        self.progress = 0
        self.status = "WAITING"         # WAITING, IN_PROGRESS, DONE[cite: 2]

    def get_name(self) -> str:
        return self.name

    def get_type(self) -> str:
        return self.task_type

    def get_position(self) -> tuple[int, int]:
        return self.pos

    def get_status(self) -> str:
        return self.status

    def set_status(self, status: str) -> None:
        self.status = status

    def advance_progress(self) -> bool:
        """Increment progress by 1 timestep. Return True when finished."""
        self.progress += 1
        if self.progress >= self.duration:
            self.__status = "DONE"
            return True
        return False