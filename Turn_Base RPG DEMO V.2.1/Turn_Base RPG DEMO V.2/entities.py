
# entities.py
import random

# Superclass untuk semua unit yang hidup
class Entity:
    def __init__(self, name, hp, atk, defe, spd):
        self.name = name
        self.base_hp = hp
        self.base_atk = atk
        self.base_defe = defe
        self.base_spd = spd
        
        self.max_hp = self.base_hp
        self.atk = self.base_atk
        self.defe = self.base_defe
        self.spd = self.base_spd
        
        self.hp = self.max_hp
        self.is_alive = True
        self.status_effects = {} # e.g. {'burn': 2, 'slow': 1, 'def_down': 2, 'atk_down': 2}
        self.buffs = {} # e.g. {'atk_up': 2, 'def_up': 1}

    def take_damage(self, damage):
        print(f"[DEBUG] {self.name} menerima damage raw: {damage}") # DEBUG
        # Apply defense reduction from status effects if any
        current_defe = self.defe # Mulai dengan nilai DEF yang sudah disesuaikan buff/debuff lainnya

        if 'def_down' in self.status_effects:
            # Tingkatkan efek def_down, misalnya 40% pengurangan
            current_defe = max(0, current_defe * 0.60) 
            print(f"[DEBUG] {self.name}'s Defense berkurang karena Def_Down! DEF Efektif: {int(current_defe)}")

        final_damage = max(1, damage - current_defe)
        self.hp -= final_damage
        print(f"{self.name} menerima {final_damage} damage!")
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
            print(f"{self.name} telah kalah!")
        return final_damage

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)
        print(f"{self.name} memulihkan {int(amount)} HP.")

    def apply_status_effect(self, effect, duration):
        # Timpa jika sudah ada, atau tambahkan yang baru
        self.status_effects[effect] = duration
        print(f"{self.name} terkena efek {effect} selama {duration} giliran.")
        self._apply_stat_modifications() # Terapkan perubahan stat segera

    def apply_buff(self, buff, duration):
        # Timpa jika sudah ada, atau tambahkan yang baru
        self.buffs[buff] = duration
        print(f"{self.name} mendapat buff {buff} selama {duration} giliran.")
        self._apply_stat_modifications() # Terapkan perubahan stat segera

    def _apply_stat_modifications(self):
        # Reset ke base stats terlebih dahulu
        self.atk = self.base_atk
        self.defe = self.base_defe
        self.spd = self.base_spd
        self.max_hp = self.base_hp 

        # Jika ini karakter, terapkan stat dari senjata/item set terlebih dahulu
        if isinstance(self, Character):
            self._apply_equipment_stats() # Metode baru untuk menangani equipment

        # Terapkan buff
        if 'atk_up' in self.buffs:
            self.atk *= 1.40 # Contoh: peningkatan ATK 40% (ditingkatkan dari 30%)
            print(f"[DEBUG] {self.name} ATK buffed to {int(self.atk)}")
        if 'def_up' in self.buffs:
            self.defe *= 1.40 # Contoh: peningkatan DEF 40% (ditingkatkan dari 30%)
            print(f"[DEBUG] {self.name} DEF buffed to {int(self.defe)}")
        if 'spd_up' in self.buffs:
            self.spd *= 1.40 # Contoh: peningkatan SPD 40% (ditingkatkan dari 30%)
            print(f"[DEBUG] {self.name} SPD buffed to {int(self.spd)}")
        
        # Terapkan status effects (debuff)
        if 'atk_down' in self.status_effects:
            self.atk *= 0.60 # Contoh: penurunan ATK 40% (ditingkatkan dari 30%)
            print(f"[DEBUG] {self.name} ATK debuffed to {int(self.atk)}")
        if 'slow' in self.status_effects:
            self.spd *= 0.60 # Contoh: penurunan SPD 40% (ditingkatkan dari 30%)
            print(f"[DEBUG] {self.name} SPD debuffed to {int(self.spd)}")
        # Catatan: 'def_down' masih ditangani langsung di take_damage untuk fleksibilitas perhitungan damage.

        # Pastikan HP tidak melebihi max_hp baru
        self.hp = min(self.hp, self.max_hp)

    def tick_status(self):
        # Proses status effect di akhir giliran
        if 'burn' in self.status_effects:
            burn_dmg = int(self.max_hp * 0.05)
            self.hp -= burn_dmg
            print(f"{self.name} terbakar dan menerima {burn_dmg} damage dari Burn.")
        
        # Kurangi durasi untuk semua efek dan buff
        for effect in list(self.status_effects.keys()):
            self.status_effects[effect] -= 1
            if self.status_effects[effect] <= 0:
                del self.status_effects[effect]
                print(f"Efek {effect} pada {self.name} telah hilang.")
        
        for buff in list(self.buffs.keys()):
            self.buffs[buff] -= 1
            if self.buffs[buff] <= 0:
                del self.buffs[buff]
                print(f"Buff {buff} pada {self.name} telah hilang.")
        
        self._apply_stat_modifications() # Terapkan kembali stat setelah tick untuk mencerminkan perubahan


# Subclass untuk karakter yang dimainkan
class Character(Entity):
    def __init__(self, name, role, hp, atk, defe, spd):
        super().__init__(name, hp, atk, defe, spd)
        self.role = role
        self.energy = 0
        self.max_energy = 100
        self.aggro = 100 # Base aggro
        self.weapon = None
        self.item_set = None

    def gain_energy(self, amount):
        self.energy = min(self.max_energy, self.energy + amount)
    
    def equip(self, weapon, item_set):
        self.weapon = weapon
        self.item_set = item_set
        # Hanya panggil _apply_stat_modifications setelah equip.
        # calculate_stats sekarang menjadi bagian dari _apply_stat_modifications.
        self._apply_stat_modifications()

    # Metode ini sekarang internal dan dipanggil oleh _apply_stat_modifications
    def _apply_equipment_stats(self):
        # Terapkan stat senjata
        if self.weapon:
            for stat, value in self.weapon.stats_boost.items():
                # Pastikan ini menambah dari base_stats, bukan current_stats
                if stat == 'max_hp': self.max_hp += self.base_hp * (value / 100)
                if stat == 'atk': self.atk += self.base_atk * (value / 100)
                if stat == 'defe': self.defe += self.base_defe * (value / 100)
                if stat == 'spd': self.spd += self.base_spd * (value / 100)
                if stat == 'aggro': self.aggro += value # Aggro adalah bonus langsung

        # Terapkan stat item set (bonus 2-set)
        if self.item_set:
            for stat, value in self.item_set.bonus_2_stats.items():
                if stat == 'max_hp': self.max_hp += self.base_hp * (value / 100)
                if stat == 'atk': self.atk += self.base_atk * (value / 100)
                if stat == 'defe': self.defe += self.base_defe * (value / 100)
                if stat == 'spd': self.spd += self.base_spd * (value / 100)
        
        # Terapkan bonus 4-set untuk aggro
        if self.item_set and self.item_set.name == "Iron Sentinel": 
            self.aggro *= 1.30 

        # Pastikan HP saat ini tidak melebihi max_hp baru setelah perubahan stat
        self.hp = min(self.hp, self.max_hp)


    def display_details(self):
        print(f"\n--- {self.name} ({self.role}) ---")
        print(f"  HP: {int(self.hp)}/{int(self.max_hp)}")
        print(f"  ATK: {int(self.atk)}, DEF: {int(self.defe)}, SPD: {int(self.spd)}")
        print(f"  Weapon: {self.weapon.name if self.weapon else 'None'}")
        print(f"  Item Set: {self.item_set.name if self.item_set else 'None'}")
        
    # Metode Aksi (akan dioverride oleh class spesifik)
    def basic_attack(self, target):
        print(f"{self.name} melakukan Basic Attack ke {target.name}.")
        
        # ATK sudah diperbarui secara dinamis oleh _apply_stat_modifications
        damage = self.atk
        target.take_damage(damage)
        self.gain_energy(10)
        # Efek Storm Piercer
        if self.weapon and self.weapon.effect == 'double_attack': 
             print(f"{self.name} menyerang lagi karena Storm Piercer!") 
             target.take_damage(damage) 
             self.gain_energy(10) 
        return True # Menandakan aksi berhasil

    def skill(self, target, **kwargs):
        print(f"{self.name} menggunakan Skill!")
        self.gain_energy(20)
        return True
    
    def special(self, target, **kwargs):
        if self.energy < self.max_energy:
            print("Energi tidak cukup untuk Special!")
            return False
        print(f"{self.name} mengeluarkan serangan Spesial!")
        self.energy = 0
        return True

# --- Definisi Karakter Spesifik ---
class Zeros (Character):
    def __init__(self):
        super().__init__("Zeros", "DPS", hp=900, atk=180, defe=80, spd=110) 
    def skill(self, target, **kwargs):
        super().skill(target)
        print(f"{self.name} menggunakan 'Crimson Rush', serangan kuat yang menembus pertahanan.")
        # ATK sudah diperbarui secara dinamis
        damage = self.atk * 1.6 
        target.take_damage(damage)
        return True
    def special(self, target, **kwargs):
        if not super().special(target): return False
        print(f"{self.name} melepaskan 'Final Eclipse', serangan dahsyat ke satu target!")
        # ATK sudah diperbarui secara dinamis
        damage = self.atk * 3.5 
        target.take_damage(damage)
        return True

class Kael (Character):
    def __init__(self):
        super().__init__("Kael", "Sub-DPS", hp=950, atk=130, defe=90, spd=125) 
    def skill(self, target, **kwargs):
        super().skill(target)
        print(f"{self.name} menggunakan 'Shadow Strike', menyerang titik lemah musuh.")
        # ATK sudah diperbarui secara dinamis
        damage = self.atk * 1.4
        # Bonus damage jika target punya status negatif
        if target.status_effects:
            damage *= 1.30 
            print("Damage meningkat karena target memiliki status negatif!")
        target.take_damage(damage)
        return True
    def special(self, target, **kwargs):
        if not super().special(target): return False
        print(f"{self.name} melepaskan 'Frost Nova', membekukan musuh.")
        # ATK sudah diperbarui secara dinamis
        damage = self.atk * 2.2 
        target.take_damage(damage)
        target.apply_status_effect('slow', 2)
        return True
        
class Garen (Character):
    def __init__(self):
        super().__init__("Garen", "Tank", hp=1800, atk=70, defe=180, spd=85) 
    def skill(self, target, **kwargs):
        super().skill(target)
        print(f"{self.name} menggunakan 'Taunting Shout', memprovokasi musuh dan meningkatkan pertahanan!")
        self.aggro += 75 
        self.apply_buff('def_up', 2)
        print(f"Aggro Garen meningkat! Pertahanannya juga naik!")
        return True
    def special(self, target, **kwargs):
        if not super().special(target): return False
        # Memberikan shield ke seluruh tim
        team = kwargs.get('team')
        print(f"{self.name} melepaskan 'Guardian's Wall', memberikan shield ke seluruh tim!")
        shield_amount = self.max_hp * 0.15 
        for member in team:
            if member.is_alive:
                member.hp += shield_amount # Simple HP add as shield
                print(f"{member.name} mendapat shield sebesar {int(shield_amount)} HP.")
        return True

class Lux (Character):
    def __init__(self):
        super().__init__("Lux", "Support", hp=1000, atk=80, defe=90, spd=120) 
    def skill(self, target, **kwargs):
        super().skill(target)
        print(f"{self.name} menggunakan 'Aura of Courage', meningkatkan ATK seluruh tim.")
        team = kwargs.get('team')
        for member in team:
            if member.is_alive:
                member.apply_buff('atk_up', 2) 
        return True
    def special(self, target, **kwargs):
        if not super().special(target): return False
        print(f"{self.name} melepaskan 'Blessing of Light', memberikan semua buff positif ke tim!")
        team = kwargs.get('team')
        for member in team:
            if member.is_alive:
                member.apply_buff('atk_up', 2)
                member.apply_buff('def_up', 2)
                member.apply_buff('spd_up', 2)
        return True
        
class Soraka (Character):
    def __init__(self):
        super().__init__("Soraka", "Healer", hp=1100, atk=70, defe=90, spd=110) 
    def skill(self, target, **kwargs):
        super().skill(target)
        print(f"{self.name} menggunakan 'Starlight Heal', memulihkan HP satu target.")
        # ATK sudah diperbarui secara dinamis
        heal_amount = self.atk * 3.0 
        target.heal(heal_amount)
        return True
    def special(self, target, **kwargs):
        if not super().special(target): return False
        print(f"{self.name} melepaskan 'Wish', memulihkan HP seluruh tim secara masif!")
        team = kwargs.get('team')
        # ATK sudah diperbarui secara dinamis
        heal_amount = self.atk * 3.5 
        for member in team:
            if member.is_alive:
                member.heal(heal_amount)
        return True

class Veigar (Character):
    def __init__(self):
        super().__init__("Veigar", "Debuffer", hp=950, atk=100, defe=85, spd=115) 
    def skill(self, target, **kwargs):
        super().skill(target)
        print(f"{self.name} menggunakan 'Curse of Weakness', menurunkan pertahanan musuh.")
        target.apply_status_effect('def_down', 2) 
        return True
    def special(self, target, **kwargs):
        if not super().special(target): return False
        print(f"{self.name} melepaskan 'Void Plague', memberikan berbagai debuff ke musuh!")
        target.apply_status_effect('def_down', 2)
        target.apply_status_effect('atk_down', 2)
        target.apply_status_effect('slow', 1) 
        target.apply_status_effect('burn', 1)
        return True

# --- Database Karakter ---
AVAILABLE_CHARACTERS = [ 
    Zeros(), Kael(), Garen(), Lux(), Soraka(), Veigar(), 
    Character("Ashe", "Sub-DPS", 900, 115, 85, 125),
    Character("Draven", "DPS", 780, 155, 65, 115),
    Character("Braum", "Tank", 1600, 75, 160, 85),
    Character("Janna", "Support", 880, 80, 80, 130)
]

# --- Definisi Boss ---
class Boss(Entity):
    def __init__(self, name, hp, atk, defe, spd):
        super().__init__(name, hp, atk, defe, spd)
        self.enrage_threshold = 0.5

    def decide_action(self, player_team):
        # AI Sederhana: Serang target dengan aggro tertinggi
        # Pastikan hanya pemain yang hidup yang dipertimbangkan
        alive_players = [p for p in player_team if p.is_alive]
        if not alive_players:
            return # Tidak ada target tersisa

        # Tentukan target berdasarkan aggro
        highest_aggro_target = max(alive_players, key=lambda p: p.aggro)
        
        # Cek untuk aksi khusus (enrage)
        if self.hp < self.max_hp * self.enrage_threshold:
            self.special_action(player_team)
        else:
            self.basic_attack(highest_aggro_target)

    def basic_attack(self, target):
        print(f"\nBOSS TURN: {self.name} menyerang {target.name}!")
        
        # ATK sudah diperbarui secara dinamis oleh _apply_stat_modifications
        damage = self.atk
        target.take_damage(damage)

    def special_action(self, player_team):
        print(f"BOSS TURN: {self.name} marah dan menggunakan skill spesial!")
        # Implementasi skill spesial boss di sini
        pass

class StoneGolem(Boss):
    def __init__(self):
        # Menyesuaikan stats boss agar lebih seimbang
        super().__init__("Ancient Stone Golem", hp=1200, atk=200, defe=50, spd=70) # Sedikit mengurangi HP/ATK/DEF boss
    def special_action(self, player_team):
        print(f"{self.name} menggunakan 'Earthquake'! Menyerang semua karakter.")
        for player in player_team:
            if player.is_alive:
                # ATK sudah diperbarui secara dinamis
                player.take_damage(self.atk * 0.7) 

class VoidDragon(Boss):
    def __init__(self):
        # Menyesuaikan stats boss agar lebih seimbang
        super().__init__("Void Dragon", hp=1400, atk=250, defe=50, spd=120) # Sedikit mengurangi HP/DEF boss, ATK masih tinggi
        self.enrage_threshold = 0.6 
    def special_action(self, player_team):
        print(f"{self.name} menggunakan 'Corrupting Breath'! Menyerang dan memberi debuff.")
        target = random.choice([p for p in player_team if p.is_alive])
        # ATK sudah diperbarui secara dinamis
        target.take_damage(self.atk * 1.2) 
        target.apply_status_effect('burn', 2) # Mengurangi durasi debuff
        target.apply_status_effect('def_down', 2) # Mengurangi durasi debuff

class CelestialArbiter(Boss):
    def __init__(self):
        # Menyesuaikan stats boss agar lebih seimbang
        super().__init__("Celestial Arbiter", hp=1500, atk=180, defe=50, spd=105) # Mengurangi HP/ATK/DEF boss
    def special_action(self, player_team):
        print(f"{self.name} menggunakan 'Judgment'! Menghapus buff tim dan menyerang.")
        for player in player_team:
            player.buffs.clear()
            # Setelah menghapus buff, terapkan kembali stat dasar dan stat item
            player._apply_stat_modifications() # Hitung ulang stat untuk pemain
        print("Semua buff pemain telah dihapus!")
        target = random.choice([p for p in player_team if p.is_alive])
        # ATK sudah diperbarui secara dinamis
        target.take_damage(self.atk * 1.8) 

BOSSES = [StoneGolem(), VoidDragon(), CelestialArbiter()]
