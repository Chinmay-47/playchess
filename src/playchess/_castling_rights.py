from dataclasses import dataclass


@dataclass
class CastlingRights:

    white_king_side: bool
    white_queen_side: bool
    black_king_side: bool
    black_queen_side: bool
