import random
import time
class Character:
    def __init__(self, name, max_hp, attack, defense, mana):
        self.name = name
        self.current_hp = max_hp
        self.max_hp = max_hp
        self.base_attack = attack
        self.defense = defense
        self.weapon = None
        self.buff_turns = 0
        self.heals_remaining = 2
        self.dodge_chance = 0
        self.fortify_turns = 0
        self.max_mana = mana
        self.mana = mana
        self.shield_hp = 0
        self.soul_link_turns = 0
        self.heal_block_turns = 0
        self.bleed_turns = 0
        self.smoke_screen_turns = 0
        self.evasive_roll_turns = 0
    
    def take_damage(self, damage_amount, attacker=None, ignore_defense=False):
        dodge_number = random.randint(1,100)
        if self.smoke_screen_turns > 0:
            effective_dodge = 75
        elif self.evasive_roll_turns > 0:
            effective_dodge = 60
        else : 
            effective_dodge = self.dodge_chance

        if dodge_number <= effective_dodge:
            if self.smoke_screen_turns > 0:
                print(f"{self.name} vanishes into smoke, dodging effortlessly!")
            elif self.evasive_roll_turns > 0:
                print(f"{self.name} rolls away succesfully!!")
            else :
                print(f"{self.name} dodges succesfully... wait HOW")
            return
                
        if ignore_defense:
            actual_damage = damage_amount
        else:
            actual_damage = max(1,damage_amount - self.defense)

        if self.shield_hp > 0:
            if self.shield_hp >= actual_damage:
                self.shield_hp -= actual_damage
                print(f"{self.name}'s shield absorbed all the damage. Shield remaining : {self.shield_hp} HP")
                return
            else:
                remaining_damage = actual_damage - self.shield_hp
                print(f"{self.name}'s shield breaks after absorbing {self.shield_hp} damage!!")
                self.shield_hp = 0
                actual_damage = remaining_damage

        if self.fortify_turns > 0:
            actual_damage = int(actual_damage*0.7)
            self.fortify_turns -=1

        self.current_hp -= actual_damage
        self.current_hp = max(0, self.current_hp)
        print(f"{self.name} has taken {actual_damage} damage and has {self.current_hp} HP left.")
        if self.soul_link_turns > 0 and attacker is not None:
            reflected_damage = int(0.25 * actual_damage)
            if reflected_damage > 0:
                print(f"💀 SOUL LINK reflects {reflected_damage} damage to {attacker.name}...")
                attacker.current_hp -= reflected_damage
                attacker.current_hp = max(0, attacker.current_hp)
            self.soul_link_turns -= 1

    def attack(self, target):
        total_damage = self.base_attack
        if self.weapon:
             total_damage += self.weapon.bonus_damage

        if self.buff_turns > 0:
            total_damage = int(total_damage * 1.5)
            accuracy_roll = random.randint(1,100)
            if accuracy_roll <= 33:
                print(f"{self.name}'s berserk attack HITS!")
                crit_roll = random.randint(1,100)
                if crit_roll <= 10:
                    total_damage *= 2
                    print(f"CRITICAL HIT, Double Damage!!")
                self.buff_turns -= 1
                target.take_damage(total_damage, self)
            else:
                print(f"{self.name}'s berserk attack MISSES!")
                self.buff_turns -= 1
                return
        else:
            accuracy_roll = random.randint(1,100)
            if accuracy_roll <= 85:
                print(f"{self.name} attacks {target.name}!")
                crit_roll = random.randint(1,100)
                if crit_roll <= 10:
                    total_damage *= 2
                    print("CRITICAL HIT, Double Damage!!")
                target.take_damage(total_damage, self)                
            else:
                print(f"{self.name} MISSED by a hair's breadth!!")
                return

    def equip_weapon(self, new_weapon):
        self.weapon = new_weapon
        print(f"{self.name} has equipped The {self.weapon.name}")

    def heal(self, heal_amount):
        if self.heal_block_turns > 0:
            print("WHAT! My healing is NOT working!!..")
            return
        if self.heals_remaining <= 0:
            print("Should've bought more healing flasks... ")
            return
        missing_hp = self.max_hp - self.current_hp
        actual_heal = min(heal_amount, missing_hp)
        self.current_hp += actual_heal
        self.heals_remaining -= 1
        print(f"{self.name} has healed a total of {actual_heal} HP. Current HP is {self.current_hp} HP")
        print(f"Heals remaining : {self.heals_remaining}")

    def berserk(self):
        self.buff_turns = 3
        print(f"{self.name} has entered a Berserk stage!")

    def is_alive(self):
        return self.current_hp > 0

        
class Weapon:
    def __init__(self, name, tier, bonus_damage):
        self.name = name
        self.tier = tier
        self.bonus_damage = bonus_damage
def generate_random_weapon():
    weapons = [
        Weapon("Rusty Dagger", "Bad", 2),
        Weapon("Chipped Sword", "Bad", 3),
        Weapon("Iron Longsword", "Decent", 4),
        Weapon("Steel Bow", "Decent", 5),
        Weapon("Flaming Greatsword", "Good", 6),
    ]
    chosen_weapon = random.choice(weapons)
    return chosen_weapon

#add new classes here-----------------------------------------------
class Mage(Character):
    def __init__(self, name):
        super().__init__(name, max_hp=80, attack=20, defense=3, mana=100)
        self.heals_remaining = 1

    def spellbook(self, target):
        print(f"\n--- {self.name}'s Spellbook ---")
        print(f"Current Mana: {self.mana}/{self.max_mana}")
        print("1. Fireball (30 Mana, 150% damage)")
        print("2. Soul Link (40 Mana, reflects 25% damage for 4 turns)")
        print("3. Heal Block (20 Mana, prevents healing for 2 turns)")
        print("4. Stone Wall (35 Mana, shield absorbs 30 damage)")
        print("5. Close Spellbook")
        
        spell_choice = input("Choose a spell (1-5): ")
        print()
        
        if spell_choice == '1':
            self.fireball(target)
        elif spell_choice == '2':
            self.soul_link(target)
        elif spell_choice == '3':
            self.heal_block(target)
        elif spell_choice == '4':
            self.stonewall()
        elif spell_choice == '5':
            print("Closing spellbook...")
        else:
            print("SPELL FAILED!!")

    def fireball(self, target):
        if self.mana < 30:
            print("I'm out of mana.....")
            return
        self.mana -= 30
        total_damage = self.base_attack
        if self.weapon:
            total_damage += self.weapon.bonus_damage
        total_damage = int(1.5*total_damage)
        crit_roll = random.randint(1, 100)
        if crit_roll <= 10:
            total_damage *= 2
            print("CRITICAL HIT! The fireball explodes with devastating force!")
        print(f"{self.name} hurls a massive fireball at {target.name}!")
        target.take_damage(total_damage, self)

    def stonewall(self):
        if self.mana < 35:
            print("I'm out of mana.....")
            return
        self.mana -= 35
        self.shield_hp = 30
        print(f"{self.name} conjured up a Stone Wall! Absorbs 30 damage before breaking! ")

    def soul_link(self, target):
        if self.mana < 40:
            print("I'm out of mana.....")
            return 
        if hasattr(target, 'debuff_immunity_turns') and target.debuff_immunity_turns > 0:
            print(f"{target.name}'s IRON WILL is unbreakable!! SOUL LINK cannot be forged...")
            self.mana -= 40
            return
        self.mana -= 40
        self.soul_link_turns = 4
        print(f"💀 {self.name} casts SOUL LINK, for 4 turns 25% of all damage taken is reflected back!")

    def heal_block(self, target):
        if self.mana < 20:
            print("I'm out of mana.....")
            return
        if hasattr(target, 'debuff_immunity_turns') and target.debuff_immunity_turns > 0:
            print(f"{target.name} has an IRON WILL, the curse couldn't be inflicted....")
            self.mana -= 20
            return        
        self.mana -= 20
        target.heal_block_turns = 2
        print(f"{self.name} CURSED {target.name} with HEAL BLOCK for 2 turns!!")

class Archer(Character):
    def __init__(self, name):
        super().__init__(name, max_hp=100, attack=15, defense=5, mana=50)

    def rangers_arsenal(self, target):
        print(f"\n--- {self.name}'s Arsenal ---")
        print("1. Arrow Volley (20 Focus, shoots 3 arrow consecutively each dealing 70% of a normal attack)")
        print("2. Shatterguard (25 Focus, ignores defense)")
        print("3. Evasive roll (15 Focus, increases dodge chance to 60% for 2 turns)")
        print("4. Distracted...")
                
        spell_choice = input("Choose a technique (1-4): ")
        print()
                
        if spell_choice == '1':
            self.arrow_volley(target)
        elif spell_choice == '2':
            self.shatterguard(target)
        elif spell_choice == '3':
            self.evasive_roll()
        elif spell_choice == '4':
            print("I need to focus...")
        else:
            print("I need to focus...")
    
    def arrow_volley(self, target):
        if self.mana < 20:
            print("My visions blurry, my hands are shaking, I can't do that right now!")
            return
        self.mana -= 20         
        print(f"{self.name} fires a volley of arrows!!")
        base_damage = self.base_attack
        if self.weapon:
            base_damage += self.weapon.bonus_damage
        arrow_damage = int(base_damage*0.7)
        hits = 0
        for i in range(3):
            accuracy_roll = random.randint(1,100)
            if accuracy_roll <= 85:
                print(f"Arrow {i+1} HITS for {arrow_damage} damage!!")
                target.take_damage(arrow_damage, self)
                hits += 1
            else:
                print(f"Arrow {i+1} MISSED...")
        print(f"{self.name} put {hits} arrows on the opponent's body!")

    def shatterguard(self, target):
        if self.mana < 25:
            print("Crap.. I can't focus...")
            return
        self.mana -= 25
        print(f"{self.name} fires a DEADLY SHOT, it PIERCES through {target.name}'s armor!!")
        total_damage = self.base_attack
        if self.weapon:
            total_damage += self.weapon.bonus_damage
        total_damage = int(total_damage*1.3)
        accuracy_roll = random.randint(1,100)
        if accuracy_roll <= 85:
            print(f"{self.name}'s shot PIERCES through and deals a fatal damage")
            target.take_damage(total_damage, self, ignore_defense=True)
        else:
            print(f"The arrow barely passes {target.name}, gotta aim better....")

    def evasive_roll(self):
        if self.mana < 15:
            print("Oh no, I can't focus...")
            return
        self.mana -= 15
        print(f"{self.name} prepares against incoming attack!!")
        self.evasive_roll_turns = 2

class Knight(Character):
    def __init__(self, name):
        super().__init__(name, max_hp=120, attack=12, defense=8, mana=0)
        self.concussive_blow_cooldown = 0
        self.iron_will_cooldown = 0
        self.debuff_immunity_turns = 0
    def grand_order_arts(self, target):
        print(f"\n--- {self.name}'s Grand Order Arts ---")
        print("1. Fortify (Reduces damage by 30% for 4 turns)")
        if self.concussive_blow_cooldown > 0:
            print(f"2. Concussive Blow (Cooldown left: {self.concussive_blow_cooldown})")
        else:
            print("2. Concussive Blow (Deals basic damage while reducing enemy's focus/mana/stamina by 20, 4 turn cooldown) -- READY")
        if self.iron_will_cooldown > 0:
            print(f"3. Iron Will (Cooldown left: {self.iron_will_cooldown})")
        else:
            print("3. Iron Will (Purges debuffs and 2 turn immunity, 5 turn cooldown) -- READY")
        print("4. Hesitate")
            
        spell_choice = input("Choose an action (1-4): ")
        print()
            
        if spell_choice == '1':
            self.fortify()
        elif spell_choice == '2':
            self.concussive_blow(target)
        elif spell_choice == '3':
            self.iron_will(target)
        elif spell_choice == '4':
            print("I missed my chance...")
        else:
            print("I missed my chance...")

    def fortify(self):
        self.fortify_turns = 4
        print(f"Knight {self.name} takes a defensive stance!! Damage reduced by 30% for the next 4 turns!")
    def concussive_blow(self, target):
        if self.concussive_blow_cooldown > 0:
            print("I can't feel my arms, I need to rest first before doing this move...")
            return
        total_damage = self.base_attack
        if self.weapon:
            total_damage += self.weapon.bonus_damage

        accuracy_roll = random.randint(1,100)
        if accuracy_roll <= 85:
            print(f"{self.name} deals a CONCUSSIVE blow!!")
            target.take_damage(total_damage, self)
            drain_amount = min(20,target.mana)
            target.mana -= drain_amount
            print(f"Concussive blow disrupts the {target.name}'s rythmn by {drain_amount} points...")
        else:
            print(f"{target.name} weaves a possibly concussive blow!!")
        self.concussive_blow_cooldown = 4
        print("I need rest my arms for 4 (turns) minutes...")

    def iron_will(self, target):
        if self.iron_will_cooldown > 0:
            print("I need more time to compose myself...")
            return
        if hasattr(target, 'soul_link_turns') and target.soul_link_turns > 0:
            target.soul_link_turns = 0
            print(f"⛓️ {self.name}'s Iron Will SHATTERS {target.name}'s SOUL LINK!")
        
        self.bleed_turns = 0
        self.heal_block_turns = 0
        self.debuff_immunity_turns = 2
        self.iron_will_cooldown = 5
        
        print(f"💪 {self.name} invokes IRON WILL!")
        print("All curses are purged! Immune to new debuffs for 2 turns!")
        
class Assassin(Character):
    def __init__(self,name):
        super().__init__(name, max_hp=85, attack=18, defense=1, mana=30)
    def assassination_art(self, target):
        print(f"\n--- {self.name}'s Assassination Art ---")
        print(f"Current Stamina: {self.mana}/{self.max_mana}")
        print("1. Cripple (20 Stamina, applies bleed)")
        print("2. Backstab (25 Stamina, 2x damage if enemy is bleeding)")
        print("3. Smoke Screen (20 Stamina, 75% dodge for 2 turns)")
        print("4. Coup de Grace (30 Stamina, 3x damage if enemy <30% HP)")
        print("5. Close")
        
        tech_choice = input("Choose a technique (1-5): ")
        print()
        
        if tech_choice == '1':
            self.cripple(target)
        elif tech_choice == '2':
            self.backstab(target)
        elif tech_choice == '3':
            self.smoke_screen()
        elif tech_choice == '4':
            self.coup_de_grace(target)
        elif tech_choice == '5':
            print("Closing assassination art...")
        else:
            print("TECHNIQUE FAILED!!")

    def cripple(self, target):
        if self.mana < 20:
            print("Not enough stamina...")
            return
        total_damage = self.base_attack
        if self.weapon:
            total_damage += self.weapon.bonus_damage
        accuracy_roll = random.randint(1, 100)
        if accuracy_roll <= 85:
            print(f"{self.name} slashes, targeting {target.name}'s vital area !")
            if hasattr(target, 'debuff_immunity_turns') and target.debuff_immunity_turns > 0:
                print(f"{target.name} has an IRON WILL, the mark and wounds cannot be inflicted")
                target.take_damage(total_damage, self)
                self.mana -= 20
                return
            shield_will_block = (target.shield_hp >= total_damage)
            target.take_damage(total_damage, self)
            if not shield_will_block:
                target.bleed_turns = 3
                print(f"🩸 {target.name} is now MARKED and BLEEDING! They will take 8 damage per turn for 3 turns!")
            else:
                print(f"{target.name}'s shield protected them from the wound!")
        else:
            print(f"{self.name}'s cripple attack MISSED!")
        self.mana -= 20    
    def backstab(self, target):
        if self.mana < 25:
            print("I can't move my legs...")
            return
        if target.bleed_turns <= 0:
            print("It's too early, they are anticipating my actions...")
            return
        total_damage = self.base_attack
        if self.weapon:
            total_damage += self.weapon.bonus_damage
        total_damage = int(total_damage * 2)
        print(f"{self.name} strikes from the shadows, targeting the wound!")
        print(f"DEVASTATING BACKSTAB! {target.name} takes {total_damage} damage!")
        target.take_damage(total_damage, self)
        target.bleed_turns = 0
        print(f"The wound is struck! Mark dissappears...")
        self.mana -= 25

    def smoke_screen(self):
        if self.mana < 20:
            print("I can't move my legs...")
            return
        self.mana -= 20
        self.smoke_screen_turns = 2
        print(f"A smoke screen is spreading near {self.name}")

    def coup_de_grace(self, target):
        if self.mana < 30:
            print("I can't move my legs...")
            return
        if target.current_hp > target.max_hp * 0.3:
            print(f"{target.name} is not weakened enough! (Need them below 30% HP)")
            return
        total_damage = self.base_attack
        if self.weapon:
            total_damage += self.weapon.bonus_damage
        total_damage = int(total_damage * 3)
        print(f"{self.name} delivers the final blow with ruthless precision!")
        print(f"COUP DE GRACE! {target.name} takes {total_damage} damage!")
        target.take_damage(total_damage, self)
        self.mana -= 30        

def choose_class(player_number):
    print(f"\n--- Player {player_number}, choose your class ---")
    print("1. Mage")
    print("2. Archer")
    print("3. Knight")
    print("4. Assassin")
    choice = input("Wanderer, pick wisely... : ")
    name = input(f"Enter Player {player_number}'s name : ")
    if choice == '1':
        return Mage(name)
    if choice == '2':
        return Archer(name)
    if choice == '3':
        return Knight(name)
    if choice == '4':
        return Assassin(name)
    
    else:
        print('Indecisive huh.. You look suited for Archery')
        return Archer(name)

    
def play_game(player1,player2):
    print(f"\n{'='*50}")
    print("May the best player win")
    print(f"{player1.name} vs {player2.name}")
    print(f"\n{'='*50}")

    player1.equip_weapon(generate_random_weapon())
    player2.equip_weapon(generate_random_weapon())

    current_turn = 1

    while player1.is_alive() and player2.is_alive():
        print(f"\n--- Turn {current_turn} ---")
        print(f"\n{player1.name}'s turn:")
        
        if player1.mana < player1.max_mana:
            mana_regen = 15
            player1.mana = min(player1.max_mana, player1.mana + mana_regen)
        if player1.heal_block_turns > 0:
            player1.heal_block_turns -= 1
        if player1.bleed_turns > 0:
            bleed_damage = 8
            player1.current_hp -= bleed_damage
            player1.current_hp = max(0, player1.current_hp)
            player1.bleed_turns -= 1
            print(f"🩸 {player1.name} takes {bleed_damage} bleed damage! HP: {player1.current_hp}/{player1.max_hp}")
        if isinstance(player1, Knight) and player1.concussive_blow_cooldown > 0:
            player1.concussive_blow_cooldown -= 1
        if isinstance(player1, Knight) and player1.debuff_immunity_turns > 0:
            player1.debuff_immunity_turns -= 1
        if player1.smoke_screen_turns > 0:
            player1.smoke_screen_turns -= 1
        if player1.evasive_roll_turns > 0:
            player1.evasive_roll_turns -= 1

        print(f"{player1.name}'s current HP : {player1.current_hp}/{player1.max_hp}")
        if isinstance(player1, Mage):
            print(f"{player1.name}'s Mana: {player1.mana}/{player1.max_mana}")
        elif isinstance(player1, Archer):
            print(f"{player1.name}'s Focus: {player1.mana}/{player1.max_mana}")
        elif isinstance(player1, Assassin):
            print(f"{player1.name}'s Stamina: {player1.mana}/{player1.max_mana}")
        print("1. Attack")
        print("2. Heal")
        print("3. Berserk")
        if isinstance(player1, Knight):
            print("4. Grand Order Arts")
        if isinstance(player1, Archer):
            print("4. Ranger's Arsenal")
        if isinstance(player1, Mage):
            print("4. Open Spellbook")
        if isinstance(player1, Assassin):
            print("4. Assassination Arts")        

        if isinstance(player1, Knight):
            choice = input("What will you do? (1/2/3/4) : ")
            print()
        elif isinstance(player1, Archer):
            choice = input("What will you do? (1/2/3/4) : ")
            print()
        elif isinstance(player1, Mage):
            choice = input("What will you do? (1/2/3/4) : ")
            print()
        elif isinstance(player1, Assassin):
            choice = input("What will you do? (1/2/3/4) : ")
            print()
        else:
            choice = input("What will you do? (1/2/3) : ")
            print()

        if choice == '1':
            player1.attack(player2)
        elif choice == '2':
            random_heal_amount = random.randint(20,40)
            player1.heal(random_heal_amount)
        elif choice == '3':
            player1.berserk()
        elif choice == '4':
            if isinstance(player1, Knight):
                player1.grand_order_arts(player2)
            elif isinstance(player1, Archer):
                player1.rangers_arsenal(player2)
            elif isinstance(player1, Mage):
                player1.spellbook(player2)
            elif isinstance(player1, Assassin):
                player1.assassination_art(player2)
        else:
            print("What a massive waste of precious time...")
        time.sleep(3)

        if not player2.is_alive():
            break

        print(f"\n{player2.name}'s turn:")

        if player2.mana < player2.max_mana:
            mana_regen = 15
            player2.mana = min(player2.max_mana, player2.mana + mana_regen)
        if player2.heal_block_turns > 0:
            player2.heal_block_turns -= 1
        print(f"{player2.name}'s current HP : {player2.current_hp}/{player2.max_hp}")
        if player2.bleed_turns > 0:
            bleed_damage = 8
            player2.current_hp -= bleed_damage
            player2.current_hp = max(0, player2.current_hp)
            player2.bleed_turns -= 1
            print(f"🩸 {player2.name} takes {bleed_damage} bleed damage! HP: {player2.current_hp}/{player2.max_hp}")
        if isinstance(player2, Knight) and player2.concussive_blow_cooldown > 0:
            player2.concussive_blow_cooldown -= 1            
        if isinstance(player2, Knight) and player2.debuff_immunity_turns > 0:
            player2.debuff_immunity_turns -= 1
        if player2.smoke_screen_turns > 0:
            player2.smoke_screen_turns -= 1
        if player2.evasive_roll_turns > 0:
            player2.evasive_roll_turns -= 1

        if isinstance(player2, Mage):
            print(f"{player2.name}'s Mana: {player2.mana}/{player2.max_mana}")
        elif isinstance(player2, Archer):
            print(f"{player2.name}'s Focus: {player2.mana}/{player2.max_mana}")
        elif isinstance(player2, Assassin):
            print(f"{player2.name}'s Stamina: {player2.mana}/{player2.max_mana}")
        print("1. Attack")
        print("2. Heal")
        print("3. Berserk")
        if isinstance(player2, Knight):
            print("4. Grand Order Arts")
        if isinstance(player2, Archer):
            print("4. Ranger's Arsenal")
        if isinstance(player2, Mage):
            print("4. Open Spellbook")
        if isinstance(player2, Assassin):
            print("4. Assassination Arts")              

        if isinstance(player2, Knight):
            choice = input("What will you do? (1/2/3/4) : ")
            print()
        elif isinstance(player2, Archer):
            choice = input("What will you do? (1/2/3/4) : ")
            print()
        elif isinstance(player2, Mage):
            choice = input("What will you do? (1/2/3/4) : ")
            print()
        elif isinstance(player2, Assassin):
            choice = input("What will you do? (1/2/3/4) : ") 
            print()          
        else:
            choice = input("What will you do? (1/2/3) : ")
            print()

        if choice == '1':
            player2.attack(player1)
        elif choice == '2':
            random_heal_amount = random.randint(20,40)
            player2.heal(random_heal_amount)
        elif choice == '3':
            player2.berserk()
        elif choice == '4':
            if isinstance(player2, Knight):
                player2.grand_order_arts(player1)
            elif isinstance(player2, Archer):
                player2.rangers_arsenal(player1)   
            elif isinstance(player2, Mage):
                player2.spellbook(player1)  
            elif isinstance(player2, Assassin):
                player2.assassination_art(player1)     
        else:
            print("What a massive waste of precious time...")
        time.sleep(3)
        
        if not player1.is_alive():
            break

        current_turn += 1

    print(f"\n{'='*50}")
    if player1.is_alive():
        print(f"{player1.name} prevails...")
    else:
        print(f"{player2.name} prevails...")
    print(f"\n{'='*50}")

# Create the fighters
player1 = choose_class(1)
player2 = choose_class(2)

# Start the battle
play_game(player1, player2)


