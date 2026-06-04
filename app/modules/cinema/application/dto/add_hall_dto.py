from dataclasses import dataclass


@dataclass(frozen=True)
class AddHallDTO:
    hall_name: str
    rows: int
    seats_per_row: int
