
class CastlingRights:
    """Class represents castling rights in chess."""

    def __init__(self, white_king_side: bool, white_queen_side: bool, black_king_side: bool, black_queen_side: bool):

        self.white_king_side = white_king_side
        self.white_queen_side = white_queen_side
        self.black_king_side = black_king_side
        self.black_queen_side = black_queen_side
