from constants import FINISH_LINE_X

def update_game(game_data, dt, assets):
    if game_data["state"] == "INTRO":
        for char in game_data["intro_chars"]:
            char.state = "running"
            char.update(dt)
            if char.pos.x > 1000: 
                char.pos.x = -64
        return
    
    if game_data.get("winner_char") is not None:
        game_data["winner_char"].update(dt)

    if game_data["state"] != "GAME": return

    for char in game_data["chars"]:
        char.update(dt)

    for char in game_data["chars"]:
        char.update_ai(dt)

    for jid, label in game_data["char_mapping"].items():
        joy = game_data["joysticks"].get(jid)
        if joy:
            p_idx = int(label[1:]) - 1
            p = game_data["players"][p_idx]
            p.update(joy, dt)

    for i, char in enumerate(game_data["chars"]):
        if char.pos.x + 20 > FINISH_LINE_X and char.state != "is_dead":
            game_data["state"] = "GAME OVER"
            assets["well_done_sound"].play()
            game_data["winner_char"] = char

            if char.is_player:
                for p in game_data["players"]:
                    if p.char_idx == i:
                        game_data["winner"] = p.label
                        break
            else:
                game_data["winner"] = "NOBODY"