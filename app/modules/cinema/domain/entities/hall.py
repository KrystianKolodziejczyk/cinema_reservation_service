from dataclasses import dataclass


@dataclass
class Hall:
    hall_id: int | None
    hall_name: str
    rows: int
    seats_per_row: int
