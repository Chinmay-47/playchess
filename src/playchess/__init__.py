from playchess.driver import play


class PlayChess:
    """Convenience class to play all game modes."""

    @staticmethod
    def play_material_bot():
        """Gets the most material advantage for 1 move with basic and minimal positional scoring."""
        play(player1="human", player2="bot", ai="material")

    @staticmethod
    def play_human():
        """Play another human."""
        play(player1="human", player2="human")

    @staticmethod
    def play_minmax_bot(pruning: bool = False, depth: int = 3):
        """Play against a MinMax bot with optional move pruning."""

        if not pruning:
            play(player1="human", player2="bot", ai="minmax", depth=depth)
            return

        play(player1="human", player2="bot", ai="minmax_pruned", depth=depth)

    @staticmethod
    def play_random_bot():
        """Play against a bot that makes random moves."""
        play(player1="human", player2="bot", ai="random")
