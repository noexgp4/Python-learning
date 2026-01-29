class BattleEntity:
    def __init__(self, name, hp, max_hp, atk, def_val, spd):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.atk = atk
        self.def_val = def_val
        self.spd = spd

    @classmethod
    def from_game_state(cls, game_state):
        return cls(
            name=game_state.job_name,
            hp=game_state.player_hp,
            max_hp=game_state.max_hp,
            atk=game_state.attack,
            def_val=game_state.defense,
            spd=game_state.spd
        )
