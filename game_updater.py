from constants import FINISH_LINE_X

def update_game(game_data, dt, assets):
    if game_data["state"] != "GAME": return

    # 1. ALLE CHARAKTERE AKTUALISIEREN
    # Hier passiert jetzt Animation, Bewegung und Hitbox-Update automatisch!
    for char in game_data["chars"]:
        char.update(dt)

    # 2. KI-LOGIK (Nur für Charaktere, die keine Spieler sind)
    for char in game_data["chars"]:
        char.update_ai(dt)

    # 3. CROSSHAIR / FADENKREUZ BEWEGUNG
    for jid, label in game_data["char_mapping"].items():
        joy = game_data["joysticks"].get(jid)
        if joy:
            p_idx = int(label[1:]) - 1 # Label ist "P1", "P2" etc.
            p = game_data["players"][p_idx]
            
            # Bewegung berechnen
            p.update(joy, dt)

    # 4. SIEG-PRÜFUNG
    for i, char in enumerate(game_data["chars"]):
        # Hat jemand das Ziel erreicht?
        if char.pos.x + 20 > FINISH_LINE_X and char.state != "is_dead":
            game_data["state"] = "GAME OVER"
            assets["well_done_sound"].play()
            
            if char.is_player:
                # Herausfinden, welcher Spieler den Sieg-Charakter steuert
                for p in game_data["players"]:
                    if p.char_idx == i:
                        game_data["winner"] = p.label
                        break
            else:
                game_data["winner"] = "NOBODY"