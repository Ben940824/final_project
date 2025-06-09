import json
from game.game import setup_config, start_poker
from agents.call_player import setup_ai as call_ai
from agents.random_player import setup_ai as random_ai
from agents.console_player import setup_ai as console_ai
from baseline0 import setup_ai as baseline0_ai

# Run 100 times and compare the results

for i in range(100):
    config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
    config.register_player(name="p1", algorithm=baseline0_ai())
    config.register_player(name="p2", algorithm=random_ai())
    game_result = start_poker(config, verbose=1)
    print(f"Game {i+1} result: {json.dumps(game_result, indent=4)}")



# config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
# config.register_player(name="p1", algorithm=baseline0_ai())
# config.register_player(name="p2", algorithm=())

## Play in interactive mode if uncomment
#config.register_player(name="me", algorithm=console_ai())
game_result = start_poker(config, verbose=1)

print(json.dumps(game_result, indent=4))
