import pygame
import sys

BUTTON_MAPPING = {
    "shoot": 3,
    "move": 0,
    "run": 1,
    "taunt": 2,
    "confirm": 6
}

def event_handler(game_data):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            jid = joy.get_instance_id()
            game_data["joysticks"][jid] = joy
            
            all_jids = sorted(game_data["joysticks"].keys())
            game_data["char_mapping"] = {}
            
            for i, current_jid in enumerate(all_jids):
                if i < len(game_data["players"]):
                    game_data["char_mapping"][current_jid] = f"P{i+1}"

        if event.type == pygame.JOYDEVICEREMOVED:
            jid = event.instance_id
            if jid in game_data["joysticks"]:
                del game_data["joysticks"][jid]
            _update_mappings(game_data)

        if game_data["state"] == "GAME OVER":
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == BUTTON_MAPPING["confirm"]:
                    game_data["assets"]["confirm_sound"].play()
                    game_data["state"] = "RESET"

        if game_data["state"] == "INTRO":
            if event.type == pygame.JOYBUTTONDOWN:
                game_data["assets"]["confirm_sound"].play()
                num_connected = len(game_data["joysticks"])
                if num_connected >= 2:
                    for i in range(num_connected):
                        if i < len(game_data["players"]):
                            char_idx = game_data["players"][i].char_idx
                            game_data["chars"][char_idx].is_player = True
                            game_data["chars"][char_idx].assigned_player = game_data["players"][i].label

                    game_data["state"] = "GAME"
                    pygame.mixer.music.play(-1)
        elif game_data["state"] == "GAME":
            jid = getattr(event, "instance_id", None)
            player_label = game_data["char_mapping"].get(jid)
            if not player_label: continue
            
            p_idx = int(player_label[1:]) - 1
            p = game_data["players"][p_idx]
            char = p.get_character(game_data["chars"])

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == BUTTON_MAPPING["shoot"]:
                    p.shoot(game_data["chars"], game_data["assets"], game_data["players"])

                if char.state != "is_dead":
                    if event.button == BUTTON_MAPPING["move"]: char.state = "moving"
                    if event.button == BUTTON_MAPPING["run"]: char.state = "running"
                    if event.button == BUTTON_MAPPING["taunt"]: char.state = "taunt"

            if event.type == pygame.JOYBUTTONUP:
                if char.state != "is_dead" and event.button in [BUTTON_MAPPING["move"], BUTTON_MAPPING["run"], BUTTON_MAPPING["taunt"]]:
                    joy = game_data["joysticks"].get(jid)
                    
                    if joy:
                        if joy.get_button(BUTTON_MAPPING["run"]):
                            char.state = "running"
                        elif joy.get_button(BUTTON_MAPPING["move"]):
                            char.state = "moving"
                        elif joy.get_button(BUTTON_MAPPING["taunt"]):
                            char.state = "taunt"
                        else:
                            char.state = "idle"
    return True

def _update_mappings(game_data):
    all_jids = sorted(game_data["joysticks"].keys())
    game_data["char_mapping"] = {}
    for i, current_jid in enumerate(all_jids):
        if i < len(game_data["players"]):
            game_data["char_mapping"][current_jid] = f"P{i+1}"