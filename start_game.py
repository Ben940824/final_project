import json
from game.game import setup_config, start_poker
from agents.call_player import setup_ai as call_ai
from agents.random_player import setup_ai as random_ai
from agents.console_player import setup_ai as console_ai
from baseline0 import setup_ai as baseline0_ai

# Run 100 times and compare the results
# 計算 p1 籌碼比 p2 多的次數
p1_wins = 0
p2_wins = 0
for i in range(100):
    config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
    config.register_player(name="p1", algorithm=baseline0_ai())
    config.register_player(name="p2", algorithm=random_ai())
    game_result = start_poker(config, verbose=0)
    
    p1_stack = game_result['players'][0]['stack']
    p2_stack = game_result['players'][1]['stack']
    
    if p1_stack > p2_stack:
        p1_wins += 1
    elif p2_stack > p1_stack:
        p2_wins += 1

# config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
# config.register_player(name="p1", algorithm=baseline0_ai())
# config.register_player(name="p2", algorithm=())

## Play in interactive mode if uncomment
#config.register_player(name="me", algorithm=console_ai())

# game_result = start_poker(config, verbose=0)

# print(json.dumps(game_result, indent=4))

print(f"p1 wins: {p1_wins}, p2 wins: {p2_wins}")
print(f"p1 win rate: {p1_wins / 100:.2%}, p2 win rate: {p2_wins / 100:.2%}")
