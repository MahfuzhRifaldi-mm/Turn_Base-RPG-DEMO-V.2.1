# gui_main.py
import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import time

# Asumsi entities.py, items.py, battle.py ada di direktori yang sama
from entities import AVAILABLE_CHARACTERS, BOSSES, Character, Boss
from items import WEAPONS_BY_ROLE, ITEM_SETS_BY_ROLE
from battle import Battle as ConsoleBattle # Menggunakan nama berbeda agar tidak konflik


class GameGUI:
    def __init__(self, master):
        self.master = master
        master.title("RPG Pertarungan Fantasi")
        master.geometry("1000x700") # Ukuran jendela

        self.player_team = []
        self.current_boss = None

        self.create_main_menu()

    def clear_frame(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def create_main_menu(self):
        self.clear_frame()

        self.menu_frame = tk.Frame(self.master)
        self.menu_frame.pack(pady=50)

        tk.Label(self.menu_frame, text="SELAMAT DATANG DI RPG PERTARUNGAN FANTASI", font=("Arial", 24, "bold")).pack(pady=20)

        tk.Button(self.menu_frame, text="Mulai Game Baru", command=self.start_new_game, font=("Arial", 16), width=20, height=2).pack(pady=10)
        tk.Button(self.menu_frame, text="Keluar", command=self.master.quit, font=("Arial", 16), width=20, height=2).pack(pady=10)

    def start_new_game(self):
        self.select_stage_gui()

    def select_stage_gui(self):
        self.clear_frame()

        stage_frame = tk.Frame(self.master)
        stage_frame.pack(pady=20)

        tk.Label(stage_frame, text="=== PILIH STAGE ===", font=("Arial", 20, "bold")).pack(pady=10)

        for i, boss in enumerate(BOSSES):
            tk.Button(stage_frame, text=f"[{i+1}] {boss.name} (ATK: {boss.atk}, DEF: {boss.defe})",
                      command=lambda b=boss: self.set_boss_and_proceed(b),
                      font=("Arial", 14), width=40).pack(pady=5)

    def set_boss_and_proceed(self, boss):
        self.current_boss = boss
        messagebox.showinfo("Stage Dipilih", f"Anda memilih stage: {self.current_boss.name}")
        self.select_characters_gui()

    def select_characters_gui(self):
        self.clear_frame()

        char_selection_frame = tk.Frame(self.master)
        char_selection_frame.pack(pady=20)

        tk.Label(char_selection_frame, text="=== PILIH 4 KARAKTER UNTUK TIM ANDA ===", font=("Arial", 20, "bold")).pack(pady=10)

        self.character_checkboxes = []
        self.selected_chars_vars = []

        for i, char in enumerate(AVAILABLE_CHARACTERS):
            var = tk.IntVar()
            cb = tk.Checkbutton(char_selection_frame, text=f"{char.name} ({char.role})", variable=var, font=("Arial", 12))
            cb.pack(anchor="w")
            self.character_checkboxes.append(cb)
            self.selected_chars_vars.append(var)

        tk.Button(char_selection_frame, text="Konfirmasi Pilihan", command=self.confirm_character_selection,
                  font=("Arial", 14), width=20).pack(pady=20)

    def confirm_character_selection(self):
        selected_count = 0
        self.player_team = []
        for i, var in enumerate(self.selected_chars_vars):
            if var.get() == 1:
                selected_count += 1
                # Penting: Buat instance baru dari karakter untuk setiap game
                # Ini mencegah stat karakter dari persistensi antar game jika tidak di-reset
                self.player_team.append(AVAILABLE_CHARACTERS[i].__class__())

        if selected_count != 4:
            messagebox.showerror("Kesalahan", "Anda harus memilih tepat 4 karakter!")
        else:
            messagebox.showinfo("Karakter Dipilih", "4 Karakter telah dipilih.")
            self.equip_team_gui(0) # Mulai proses equipping untuk karakter pertama

    def equip_team_gui(self, char_index):
        self.clear_frame()

        if char_index >= len(self.player_team):
            messagebox.showinfo("Persiapan Selesai", "Tim Anda siap bertarung!")
            self.start_battle_gui()
            return

        character = self.player_team[char_index]

        equip_frame = tk.Frame(self.master)
        equip_frame.pack(pady=20)

        tk.Label(equip_frame, text=f"--- Melengkapi {character.name} ({character.role}) ---", font=("Arial", 18, "bold")).pack(pady=10)

        # Bagian Pilih Senjata
        tk.Label(equip_frame, text="Pilih Senjata:", font=("Arial", 14)).pack(pady=5)
        available_weapons = WEAPONS_BY_ROLE[character.role]
        self.weapon_var = tk.StringVar(equip_frame)
        self.weapon_var.set(available_weapons[0].name) # Default selection
        weapon_menu = tk.OptionMenu(equip_frame, self.weapon_var, *[w.name for w in available_weapons])
        weapon_menu.config(font=("Arial", 12), width=40)
        weapon_menu.pack(pady=5)

        # Bagian Pilih Item Set
        tk.Label(equip_frame, text="Pilih Item Set:", font=("Arial", 14)).pack(pady=5)
        available_sets = ITEM_SETS_BY_ROLE[character.role]
        self.item_set_var = tk.StringVar(equip_frame)
        self.item_set_var.set(available_sets[0].name) # Default selection
        item_set_menu = tk.OptionMenu(equip_frame, self.item_set_var, *[s.name for s in available_sets])
        item_set_menu.config(font=("Arial", 12), width=40)
        item_set_menu.pack(pady=5)

        def confirm_equip():
            selected_weapon_name = self.weapon_var.get()
            selected_set_name = self.item_set_var.get()

            selected_weapon = next(w for w in available_weapons if w.name == selected_weapon_name)
            selected_set = next(s for s in available_sets if s.name == selected_set_name)

            character.equip(selected_weapon, selected_set)
            messagebox.showinfo("Berhasil Melengkapi", f"{character.name} berhasil dilengkapi!")
            self.equip_team_gui(char_index + 1) # Lanjut ke karakter berikutnya

        tk.Button(equip_frame, text="Lengkapi", command=confirm_equip, font=("Arial", 14), width=20).pack(pady=20)


    def start_battle_gui(self):
        self.clear_frame()

        # Kelas Battle baru yang berinteraksi dengan GUI
        self.battle_gui_instance = BattleGUI(self.master, self.player_team, self.current_boss)
        self.battle_gui_instance.run_battle()

    def end_game_options(self, win):
        self.clear_frame()
        end_frame = tk.Frame(self.master)
        end_frame.pack(pady=50)

        if win:
            tk.Label(end_frame, text="SELAMAT, ANDA MENANG!", font=("Arial", 24, "bold"), fg="green").pack(pady=20)
        else:
            tk.Label(end_frame, text="ANDA KALAH...", font=("Arial", 24, "bold"), fg="red").pack(pady=20)

        tk.Button(end_frame, text="Coba Lagi Stage Ini", command=self.restart_current_stage, font=("Arial", 16), width=25).pack(pady=10)
        tk.Button(end_frame, text="Pilih Stage Lain", command=self.select_stage_gui, font=("Arial", 16), width=25).pack(pady=10)
        tk.Button(end_frame, text="Keluar dari Game", command=self.master.quit, font=("Arial", 16), width=25).pack(pady=10)

    def restart_current_stage(self):
        # Reset HP/status untuk replay
        for char in self.player_team:
            char.hp = char.max_hp
            char.is_alive = True
            char.status_effects.clear()
            char.buffs.clear() # Reset buffs juga
            char.energy = 0 # Reset energy
        
        # Buat instance baru dari boss agar statnya juga reset
        self.current_boss = self.current_boss.__class__() 
        self.start_battle_gui()


class BattleGUI:
    def __init__(self, master, player_team, boss):
        self.master = master
        self.player_team = player_team
        self.boss = boss
        self.game_objects = self.player_team + [self.boss]
        self.turn_order = sorted(self.game_objects, key=lambda x: x.spd, reverse=True)
        self.skill_points = 3
        self.max_skill_points = 5
        self.turn_count = 0
        
        # Referensi kembali ke GameGUI untuk end_game_options
        self.game_gui_ref = master.winfo_toplevel()._data["game_gui_instance"]

        self.create_battle_ui()
        
    def create_battle_ui(self):
        # Frame untuk UI Utama Pertarungan
        self.battle_frame = tk.Frame(self.master)
        self.battle_frame.pack(fill="both", expand=True)

        # Top Section: Boss Status
        self.boss_status_frame = tk.LabelFrame(self.battle_frame, text="BOSS STATUS", font=("Arial", 14))
        self.boss_status_frame.pack(pady=10, fill="x", padx=20)
        self.boss_hp_label = tk.Label(self.boss_status_frame, text="", font=("Arial", 12))
        self.boss_hp_label.pack(pady=5)

        # Middle Section: Player Team Status
        self.player_team_frame = tk.LabelFrame(self.battle_frame, text="PLAYER TEAM", font=("Arial", 14))
        self.player_team_frame.pack(pady=10, fill="x", padx=20)
        self.char_labels = []
        for char in self.player_team:
            label = tk.Label(self.player_team_frame, text="", font=("Arial", 10))
            label.pack(anchor="w")
            self.char_labels.append(label)

        # Bottom Section: Action and Log
        self.action_log_frame = tk.Frame(self.battle_frame)
        self.action_log_frame.pack(pady=10, fill="both", expand=True, padx=20)

        self.action_frame = tk.LabelFrame(self.action_log_frame, text="AKSI", font=("Arial", 14))
        self.action_frame.pack(side="left", fill="both", expand=False, padx=10)

        self.log_frame = tk.LabelFrame(self.action_log_frame, text="LOG PERTARUNGAN", font=("Arial", 14))
        self.log_frame.pack(side="right", fill="both", expand=True, padx=10)
        self.log_text = tk.Text(self.log_frame, wrap="word", state="disabled", font=("Arial", 10))
        self.log_text.pack(fill="both", expand=True)
        self.log_scrollbar = tk.Scrollbar(self.log_frame, command=self.log_text.yview)
        self.log_scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=self.log_scrollbar.set)
        
        self.sp_label = tk.Label(self.action_frame, text=f"SKILL POINTS (SP): {self.skill_points}/{self.max_skill_points}", font=("Arial", 12))
        self.sp_label.pack(pady=5)

        self.action_buttons_frame = tk.Frame(self.action_frame)
        self.action_buttons_frame.pack(pady=10)

        self.basic_attack_btn = tk.Button(self.action_buttons_frame, text="Basic Attack (Menambah 1 SP)", command=lambda: self.player_action("basic"), font=("Arial", 10), width=30)
        self.basic_attack_btn.pack(pady=5)
        self.skill_btn = tk.Button(self.action_buttons_frame, text="Skill (Membutuhkan 1 SP)", command=lambda: self.player_action("skill"), font=("Arial", 10), width=30)
        self.skill_btn.pack(pady=5)
        self.special_btn = tk.Button(self.action_buttons_frame, text="Special (Membutuhkan 100 Energi)", command=lambda: self.player_action("special"), font=("Arial", 10), width=30)
        self.special_btn.pack(pady=5)
        self.detail_btn = tk.Button(self.action_buttons_frame, text="Lihat Detail Karakter", command=self.show_character_details, font=("Arial", 10), width=30)
        self.detail_btn.pack(pady=5)

        self.current_turn_label = tk.Label(self.action_frame, text="", font=("Arial", 12, "bold"))
        self.current_turn_label.pack(pady=10)
        
        self.update_ui() # Initial UI update

    def update_ui(self):
        self.boss_hp_label.config(text=f"BOSS: {self.boss.name} | HP: {int(self.boss.hp)}/{int(self.boss.max_hp)}")
        
        for i, char in enumerate(self.player_team):
            hp_bar = f"HP: {int(char.hp)}/{int(char.max_hp)}"
            energy_bar = f"Energy: {char.energy}/{char.max_energy}"
            status_text = ", ".join(char.status_effects.keys())
            buff_text = ", ".join(char.buffs.keys())
            status = "(K.O.)" if not char.is_alive else ""
            self.char_labels[i].config(text=f"[{i+1}] {char.name:<15} | {hp_bar:<20} | {energy_bar:<20} | Status: [{status_text}] | Buffs: [{buff_text}] {status}")
        
        self.sp_label.config(text=f"SKILL POINTS (SP): {self.skill_points}/{self.max_skill_points}")
        
    def append_log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END) # Scroll to bottom
        self.log_text.config(state="disabled")

    def run_battle(self):
        self.turn_count = 0
        self.current_entity_index = 0
        self.process_next_turn()

    def process_next_turn(self):
        if not self.boss.is_alive:
            self.append_log("Pertarungan berakhir!")
            messagebox.showinfo("Pertarungan Selesai", "Anda Menang!")
            self.game_gui_ref.end_game_options(True)
            return
        
        if not any(p.is_alive for p in self.player_team):
            self.append_log("Pertarungan berakhir!")
            messagebox.showinfo("Pertarungan Selesai", "Anda Kalah...")
            self.game_gui_ref.end_game_options(False)
            return

        self.current_turn_label.config(text=f"--- Turn {self.turn_count + 1} ---")
        
        # Find the next alive entity in turn order
        while True:
            if self.current_entity_index >= len(self.turn_order):
                self.current_entity_index = 0
                self.turn_count += 1
                self.append_log(f"\n--- Turn {self.turn_count} ---")
                
            current_entity = self.turn_order[self.current_entity_index]

            if not current_entity.is_alive:
                self.current_entity_index += 1
                continue # Skip dead entities

            self.current_turn_label.config(text=f"Giliran: {current_entity.name}")
            self.append_log(f"\nGiliran: {current_entity.name}")

            if isinstance(current_entity, Character):
                self.active_character = current_entity
                self.enable_player_actions()
                break # Wait for player input
            else: # Boss's turn
                self.disable_player_actions()
                self.master.after(1000, lambda: self.boss_turn_logic(current_entity))
                break # Process boss turn, then proceed

    def boss_turn_logic(self, boss_entity):
        boss_entity.decide_action(self.player_team)
        self.update_ui()
        self.tick_and_next_turn(boss_entity)

    def enable_player_actions(self):
        self.basic_attack_btn.config(state="normal")
        self.skill_btn.config(state="normal")
        self.special_btn.config(state="normal")
        self.detail_btn.config(state="normal")

    def disable_player_actions(self):
        self.basic_attack_btn.config(state="disabled")
        self.skill_btn.config(state="disabled")
        self.special_btn.config(state="disabled")
        self.detail_btn.config(state="disabled")

    def player_action(self, action_type):
        character = self.active_character
        
        # Overwrite print function to capture output for log_text
        original_print = __builtins__.print
        def gui_print(*args, **kwargs):
            message = " ".join(map(str, args))
            self.append_log(message)
            original_print(message, **kwargs) # Still print to console for debugging
        __builtins__.print = gui_print

        success = False
        target = None

        if action_type == "basic":
            target = self.select_target_gui([self.boss])
            if target:
                character.basic_attack(target)
                self.skill_points = min(self.max_skill_points, self.skill_points + 1)
                success = True
        elif action_type == "skill":
            if self.skill_points < 1:
                messagebox.showwarning("Tidak Cukup SP", "Skill Points tidak cukup!")
            else:
                target = self.select_target_gui(self.game_objects)
                if target:
                    # Pass team as kwargs for skill method
                    if character.skill(target, team=self.player_team):
                        self.skill_points -= 1
                        success = True
        elif action_type == "special":
            if character.energy < character.max_energy:
                messagebox.showwarning("Energi Belum Penuh", "Energi belum penuh!")
            else:
                target = self.select_target_gui(self.game_objects)
                if target:
                    if character.special(target, team=self.player_team):
                        success = True
        
        # Restore original print function
        __builtins__.print = original_print

        if success:
            self.disable_player_actions()
            self.update_ui()
            self.master.after(1000, lambda: self.tick_and_next_turn(character))
        elif target is None and action_type != "detail": # If target selection was cancelled
             self.append_log("Aksi dibatalkan.")
             # Re-enable actions if target selection was cancelled
             self.enable_player_actions()


    def select_target_gui(self, available_targets):
        valid_targets = [t for t in available_targets if t.is_alive]
        if not valid_targets:
            messagebox.showwarning("Tidak Ada Target", "Tidak ada target yang tersedia.")
            return None

        # Create a new Toplevel window for target selection
        target_window = tk.Toplevel(self.master)
        target_window.title("Pilih Target")
        target_window.transient(self.master) # Make it dependent on the main window
        target_window.grab_set() # Make it modal

        selected_target = None
        def set_and_destroy(target):
            nonlocal selected_target
            selected_target = target
            target_window.destroy()

        tk.Label(target_window, text="Pilih Target:", font=("Arial", 14)).pack(pady=10)
        for i, target in enumerate(valid_targets):
            tk.Button(target_window, text=f"[{i+1}] {target.name} ({int(target.hp)} HP)",
                      command=lambda t=target: set_and_destroy(t),
                      font=("Arial", 12), width=30).pack(pady=5)
        
        tk.Button(target_window, text="[0] Kembali", command=target_window.destroy, font=("Arial", 12), width=30).pack(pady=10)

        self.master.wait_window(target_window) # Wait for the Toplevel window to close
        return selected_target

    def show_character_details(self):
        details_window = tk.Toplevel(self.master)
        details_window.title("Detail Karakter")
        details_window.grab_set()

        tk.Label(details_window, text="--- DETAIL KARAKTER TIM ANDA ---", font=("Arial", 16, "bold")).pack(pady=10)

        for char in self.player_team:
            detail_text = f"--- {char.name} ({char.role}) ---\n" \
                          f"  HP: {int(char.hp)}/{int(char.max_hp)}\n" \
                          f"  ATK: {int(char.atk)}, DEF: {int(char.defe)}, SPD: {int(char.spd)}\n" \
                          f"  Weapon: {char.weapon.name if char.weapon else 'None'}\n" \
                          f"  Item Set: {char.item_set.name if char.item_set else 'None'}\n\n"
            tk.Label(details_window, text=detail_text, justify="left", font=("Arial", 10)).pack(anchor="w", padx=20)
        
        tk.Button(details_window, text="Tutup", command=details_window.destroy, font=("Arial", 12)).pack(pady=10)
        details_window.wait_window(details_window)
        # After closing details, re-enable player actions if it was their turn
        if isinstance(self.turn_order[self.current_entity_index], Character):
            self.enable_player_actions()


    def tick_and_next_turn(self, entity):
        # Overwrite print function to capture output for log_text
        original_print = __builtins__.print
        def gui_print(*args, **kwargs):
            message = " ".join(map(str, args))
            self.append_log(message)
            original_print(message, **kwargs) # Still print to console for debugging
        __builtins__.print = original_print

        entity.tick_status() # Apply status damage/duration reduction
        
        # Restore original print function
        __builtins__.print = original_print

        self.update_ui()
        self.current_entity_index += 1
        self.master.after(1000, self.process_next_turn) # Small delay for better UX


if __name__ == "__main__":
    root = tk.Tk()
    # Store an instance of GameGUI in root's data to access it later from BattleGUI
    root._data = {"game_gui_instance": None} 
    game_app = GameGUI(root)
    root._data["game_gui_instance"] = game_app
    root.mainloop()