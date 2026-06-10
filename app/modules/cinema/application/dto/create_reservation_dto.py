from dataclasses import dataclass


@dataclass(frozen=True)
class CreateReservationDTO:
    hold_id: int
    screening_id: int
