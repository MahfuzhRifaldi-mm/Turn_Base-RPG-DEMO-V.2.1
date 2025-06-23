# battle.py
import os
import time

from entities import Character

class Battle:
    def __init__(self, player_team, boss):
        self.player_team = player_team
        self.boss = boss
        self.game_objects = self.player_team + [self.boss]
        self.turn_order = sorted(self.game_objects, key=lambda x: x.spd, reverse=True)
        self.skill_points = 3
        self.max_skill_points = 5

    def display_ui(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("="*40)
        print("BATTLE STATUS")
        print("="*40)
        print(f"BOSS: {self.boss.name} | HP: {int(self.boss.hp)}/{int(self.boss.max_hp)}")
        print("-"*40)
        print("PLAYER TEAM:")
        for i, char in enumerate(self.player_team):
            hp_bar = f"HP: {int(char.hp)}/{int(char.max_hp)}"
            energy_bar = f"Energy: {char.energy}/{char.max_energy}"
            status = "(K.O.)" if not char.is_alive else ""
            print(f"  [{i+1}] {char.name:<15} | {hp_bar:<20} | {energy_bar:<20} {status}")
        print("-"*40)
        print(f"SKILL POINTS (SP): {self.skill_points}/{self.max_skill_points}")
        print("="*40)

    def run(self):
        turn_count = 0
        while self.boss.is_alive and any(p.is_alive for p in self.player_team):
            turn_count += 1
            print(f"\n--- Turn {turn_count} ---")
            
            for entity in self.turn_order:
                if not entity.is_alive:
                    continue

                self.display_ui()
                print(f"Giliran: {entity.name}")
                
                if isinstance(entity, Character): # Player's turn
                    self.player_turn(entity)
                else: # Boss's turn
                    entity.decide_action(self.player_team)
                    time.sleep(2)

                # Check for win/loss after each action
                if not self.boss.is_alive or not any(p.is_alive for p in self.player_team):
                    break
                
                entity.tick_status() # Apply status damage/duration reduction
                time.sleep(1)

        self.end_battle()

    def player_turn(self, character):
        while True:
            print(f"\nPilih Aksi untuk {character.name}:")
            print("1. Basic Attack (Menambah 1 SP)")
            print(f"2. Skill (Membutuhkan 1 SP)")
            print(f"3. Special (Membutuhkan 100 Energi)")
            print("4. Lihat Detail Karakter")

            choice = input("Pilihan Aksi: > ")
            if choice == "1": # Basic Attack
                target = self.select_target([self.boss])
                if target:
                    character.basic_attack(target)
                    self.skill_points = min(self.max_skill_points, self.skill_points + 1)
                    break
            elif choice == "2": # Skill
                if self.skill_points < 1:
                    print("Skill Points tidak cukup!")
                    continue
                
                # Menentukan target untuk skill (bisa musuh, bisa teman)
                target = self.select_target(self.game_objects) # Bisa target siapa saja
                if target:
                    # Mengirim seluruh team jika skill butuh (e.g. support/healer)
                    if character.skill(target, team=self.player_team):
                        self.skill_points -= 1
                        break
            elif choice == "3": # Special
                if character.energy < character.max_energy:
                    print("Energi belum penuh!")
                    continue
                
                target = self.select_target(self.game_objects)
                if target:
                    if character.special(target, team=self.player_team):
                        break
            elif choice == "4":
                for char in self.player_team:
                    char.display_details()
                input("\nTekan Enter untuk kembali...")
                self.display_ui() # Redraw UI
            else:
                print("Pilihan tidak valid.")

    def select_target(self, available_targets):
        while True:
            print("\nPilih Target:")
            # Filter hanya target yang hidup
            valid_targets = [t for t in available_targets if t.is_alive]
            for i, target in enumerate(valid_targets):
                print(f"[{i+1}] {target.name} ({int(target.hp)} HP)")
            print("[0] Kembali")
            
            try:
                choice = int(input("Pilihan Target: > "))
                if choice == 0:
                    return None
                if 1 <= choice <= len(valid_targets):
                    return valid_targets[choice - 1]
                else:
                    print("Pilihan tidak valid.")
            except ValueError:
                print("Masukkan angka.")

    def end_battle(self):
        self.display_ui()
        if not self.boss.is_alive:
            print("\n====================")
            print("  SELAMAT, ANDA MENANG! ")
            print("====================")
        else:
            print("\n====================")
            print("   ANDA KALAH...   ")
            print("====================")