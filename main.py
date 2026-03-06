from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from PIL.ImageTk import PhotoImage
import random
import os
import glob


class Player:
    def __init__(self, name, health, mana, damage, crit_damage, crit_chance):
        self.level = 1
        self.exp = 0
        self.exp_to_next_level = 100
        self.name = name
        self.health = health
        self.max_health = health
        self.mana = mana
        self.max_mana = mana
        self.damage = damage
        self.crit_damage = crit_damage
        self.crit_chance = crit_chance

    def attack(self, attack_type, enemy):
        damage_dealt = self.damage

        if random.random() < self.crit_chance:
            damage_dealt *= self.crit_damage
            crit_message = "CRIT! "
        else:
            crit_message = ""

        if attack_type == "fireball":
            if self.mana >= 10:
                self.mana -= 10
                damage_dealt = int(damage_dealt * 1.5)
                enemy.health -= damage_dealt
                return f"{crit_message} {self.name} cast fireball {damage_dealt} damage"
            else:
                return f"{self.name} not enough mana"

        elif attack_type == "iceball":
            if self.mana >= 20:
                self.mana -= 20
                damage_dealt = int(damage_dealt * 1.5)
                enemy.health -= damage_dealt
                return f"{crit_message} {self.name} cast iceball {damage_dealt} damage"
            else:
                return f"{self.name} not enough mana"

        elif attack_type == "freeze":
            if self.mana >= 50:
                self.mana -= 50
                damage_dealt = int(damage_dealt * 1.5)
                enemy.health -= damage_dealt
                return f"{crit_message} {self.name} cast freeze {damage_dealt} damage"
            else:
                return f"{self.name} not enough mana"

        elif attack_type == "melee":
            damage_dealt = int(damage_dealt * 1.5)
            enemy.health -= damage_dealt
            return f"{crit_message} {self.name} attacked melee {damage_dealt} damage"
        else:
            return f"{self.name} not enough mana"

    def gain_exp(self, amount):
        self.exp += amount
        while self.exp >= self.exp_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_next_level
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
        self.max_health += 20
        self.health = self.max_health
        self.max_mana += 15
        self.mana = self.max_mana
        self.damage += 5
        self.crit_chance = min(self.crit_chance + 0.02, 0.5)

        return f"LEVEL UP! Now level {self.level}!"


class Enemy:
    # Список возможных имен для врагов
    possible_names = [
        "Piglet", "Boar", "Wild Boar", "Giant Boar", "War Boar",
        "Demon Boar", "Hell Boar", "Ancient Boar", "Legendary Boar", "Boar King",
        "Angry Pig", "Furious Hog", "Savage Swine", "Razorback", "Tusker",
        "Forest Boar", "Mountain Pig", "Iron Hog", "Blood Boar", "Shadow Pig"
    ]

    def __init__(self, base_health, base_damage, base_exp_reward, scaling_factor=1.2):
        self.level = 1
        self.base_health = base_health
        self.base_damage = base_damage
        self.base_exp_reward = base_exp_reward
        self.scaling_factor = scaling_factor
        self.current_image = None
        self.available_images = []
        self.load_available_images()
        self.update_stats()
        self.randomize_appearance()

    def load_available_images(self):

        image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp']
        for i in image_extensions:
            self.available_images.extend(glob.glob(f"pig{i}"))
            self.available_images.extend(glob.glob(f"Pig{i}"))
            self.available_images.extend(glob.glob(f"PIG{i}"))

        if not self.available_images:
            for i in image_extensions:
                self.available_images.extend(glob.glob(f"*{i}"))

    def randomize_appearance(self):
        self.name = random.choice(self.possible_names)

        # Случайное изображение
        if self.available_images:
            self.current_image_file = random.choice(self.available_images)
        else:
            self.current_image_file = None

    def get_random_name(self):
        return random.choice(self.possible_names)

    def get_random_image(self):
        if self.available_images:
            return random.choice(self.available_images)
        return None

    def update_stats(self):
        # обновление статов врага
        self.max_health = int(self.base_health * (self.scaling_factor ** (self.level - 1)))
        self.health = self.max_health
        self.damage = int(self.base_damage * (self.scaling_factor ** (self.level - 1)))
        self.exp_reward = int(self.base_exp_reward * (self.scaling_factor ** (self.level - 1)))

    def scale_to_player_level(self, player_level):
        if self.level < player_level:
            old_level = self.level
            self.level = player_level
            self.update_stats()
            old_name = self.name
            self.randomize_appearance()
            return f"Enemy evolved from {old_name} (lvl {old_level}) to {self.name} (lvl {self.level})!"
        return None

    def respawn(self):
        self.randomize_appearance()
        self.health = self.max_health
        return f"New {self.name} (lvl {self.level}) appears!"

    def attack(self, player):
        player.health -= self.damage
        return f"{self.name} Attacked {self.damage} damage"


player = Player("Retr0sh", 100, 100, 10, 2, 0.1)
pig = Enemy(100, 10, 50, scaling_factor=1.2)

window = Tk()
window.title("RPG")
window.iconbitmap("icon.ico")
window.config(bg='black')
window.resizable(False, False)
window.geometry("960x540")
style = ttk.Style()

try:
    menu_image = PhotoImage(file="menu.png")
    menu_label = Label(window, image=menu_image)
    menu_label.place(x=0, y=0, relwidth=1, relheight=1)
except:
    window.configure(bg='black')

enemy_image_label = Label(window, bg='black')
enemy_image_label.place(x=415, y=0)


def update_enemy_image():
    try:
        if pig.current_image_file and os.path.exists(pig.current_image_file):
            pig_image_pil = Image.open(pig.current_image_file)
            pig_image = ImageTk.PhotoImage(pig_image_pil)
            enemy_image_label.config(image=pig_image)
            enemy_image_label.image = pig_image
            enemy_image_label.config(text='')
        else:
            enemy_image_label.config(text=f"{pig.name}\nLvl {pig.level}", font=("Arial", 20), fg='white', bg='gray')
            enemy_image_label.config(image='')
    except Exception as e:
        print(f"Error loading image: {e}")
        enemy_image_label.config(text=f"{pig.name}\nLvl {pig.level}", font=("Arial", 20), fg='white', bg='gray')
        enemy_image_label.config(image='')


def update_ui():
    # обновление UI
    health_bar.config(width=int(200 * (player.health / player.max_health)))
    health_text.config(text=f"{player.health}/{player.max_health}")

    mana_bar.config(width=int(140 * (player.mana / player.max_mana)))
    mana_text.config(text=f"{player.mana}/{player.max_mana}")

    damage_text.config(text=f"{player.damage}")
    crit_text.config(text=f"{int(player.crit_chance * 100)}%")

    level_text.config(text=f"Level: {player.level}")
    exp_text.config(text=f"EXP: {player.exp}/{player.exp_to_next_level}")
    exp_bar.config(width=int(130 * (player.exp / player.exp_to_next_level)))

    # проверко уселения врага
    if pig.level < player.level:
        enemy_scale_msg = pig.scale_to_player_level(player.level)
        if enemy_scale_msg:
            console_text.insert(END, enemy_scale_msg + "\n")
            console_text.insert(END, f"Health: {pig.max_health}, Damage: {pig.damage}\n")
            update_enemy_image()

    enemy_health_width = int(200 * (pig.health / pig.max_health))
    if enemy_health_width < 0:
        enemy_health_width = 0
    enemy_health_bar.config(width=enemy_health_width)
    enemy_health_text.config(text=f"{pig.health}/{pig.max_health}")
    enemy_info_text.config(text=f"{pig.name} (lvl {pig.level})")

    if pig.health <= 0:
        # получение опыта за победу
        exp_gained = pig.exp_reward
        player.gain_exp(exp_gained)
        console_text.insert(END, f"{pig.name} defeat! +{exp_gained} EXP\n")

        # восстановление после победы
        player.health = min(player.health + 20, player.max_health)
        player.mana = min(player.mana + 20, player.max_mana)

        # проверко повышения уровня
        if player.exp >= player.exp_to_next_level:
            level_up_msg = player.level_up()
            console_text.insert(END, level_up_msg + "\n")
            console_text.insert(END, f"Health +20, Mana +15, Damage +5, Crit chance +2%\n")

            # повышение уровня врага до уровня игрока
            enemy_scale_msg = pig.scale_to_player_level(player.level)
            if enemy_scale_msg:
                console_text.insert(END, enemy_scale_msg + "\n")
                console_text.insert(END, f"Health: {pig.max_health}, Damage: {pig.damage}\n")
        else:
            respawn_msg = pig.respawn()
            console_text.insert(END, respawn_msg + "\n")

        # востоновление здоровья вага
        pig.health = pig.max_health
        console_text.insert(END, "Restored 20 HP and 20 MP\n")

        update_enemy_image()
        update_ui()

    if player.health <= 0:
        player.health = 0
        console_text.insert(END, "Game over!.\n")
        mele_attack_button.config(state=DISABLED)
        fireball_button.config(state=DISABLED)
        iceball_button.config(state=DISABLED)
        freeze_button.config(state=DISABLED)
        escape_button.config(state=DISABLED)


def attack(attack_type):
    if player.health <= 0:
        console_text.insert(END, "You dead! you can't attack!\n")
        return

    if pig.health <= 0:
        console_text.insert(END, "Enemy already is dead!\n")
        return

    # атака игрока
    result = player.attack(attack_type, pig)
    console_text.insert(END, result + "\n")
    update_ui()

    # атака врага (только если враг еще жив)
    if pig.health > 0 and player.health > 0:
        enemy_result = pig.attack(player)
        console_text.insert(END, enemy_result + "\n")
        update_ui()

    console_text.see(END)


def escape():
    if player.health <= 0:
        console_text.insert(END, "You dead! you can't escape!\n")
        return

    if pig.health <= 0:
        console_text.insert(END, "Enemy already is dead!\n")
        return

    escape_chance = 0.5

    if random.random() < escape_chance:
        console_text.insert(END, "You successfully escaped from battle!\n")
        pig.health = pig.max_health
        player.health = player.max_health
        player.mana = player.max_mana

        respawn_msg = pig.respawn()
        console_text.insert(END, respawn_msg + "\n")
        console_text.insert(END, "Fully restored!\n")
        update_enemy_image()
        update_ui()
    else:
        console_text.insert(END, "Escape failed! Enemy attacks!\n")
        enemy_result = pig.attack(player)
        console_text.insert(END, enemy_result + "\n")
        update_ui()

    console_text.see(END)


# прогресс-бар health enemy
enemy_health_bar_frame = Frame(window, height=20, width=200, bg='black', relief=SUNKEN, borderwidth=1)
enemy_health_bar_frame.place(x=550, y=30)

enemy_health_bar = Frame(enemy_health_bar_frame, bg='green', height=20, width=200)
enemy_health_bar.place(x=0, y=0)

enemy_health_text = Label(window, text=f"{pig.health}/{pig.max_health}", font=("Arial", 11), bg='black', fg='red')
enemy_health_text.place(x=690, y=5)

# информация о враге
enemy_info_text = Label(window, text=f"{pig.name} (lvl {pig.level})", font=("Arial", 11), bg='black', fg='red')
enemy_info_text.place(x=550, y=5)

# прогресс-бар health player
health_bar_frame = Frame(window, height=20, width=200, bg='black', relief=SUNKEN, borderwidth=1)
health_bar_frame.place(x=180, y=100)

health_bar = Frame(health_bar_frame, bg='green', height=20, width=200)
health_bar.place(x=0, y=0)

health_text = Label(window, text=f"{player.health}/{player.max_health}", font=("Arial", 11), bg='black', fg='red')
health_text.place(x=115, y=98)

# прогресс-бар mana player
mana_bar_frame = Frame(window, height=20, width=140, bg='black', relief=SUNKEN, borderwidth=1)
mana_bar_frame.place(x=240, y=149)

mana_bar = Frame(mana_bar_frame, bg='blue', height=20, width=140)
mana_bar.place(x=0, y=0)

mana_text = Label(window, text=f"{player.mana}/{player.max_mana}", font=("Arial", 11), bg='black', fg='red')
mana_text.place(x=180, y=148)

# уровень и опыт
level_text = Label(window, text=f"Level: {player.level}", font=("Arial"), bg='black', fg='red')
level_text.place(x=180, y=40)

exp_bar_frame = Frame(window, height=15, width=130, bg='black', relief=SUNKEN, borderwidth=1)
exp_bar_frame.place(x=250, y=55)

exp_bar = Frame(exp_bar_frame, bg='purple', height=15, width=int(130 * (player.exp / player.exp_to_next_level)))
exp_bar.place(x=0, y=0)

exp_text = Label(window, text=f"EXP: {player.exp}/{player.exp_to_next_level}", font=("Arial", 8), bg='black', fg='red')
exp_text.place(x=180, y=60)

# урон
damage_text = Label(window, text=f"{player.damage}", font=("Arial", 15), bg='black', fg='red')
damage_text.place(x=230, y=195)

# крит
crit_text = Label(window, text=f"{int(player.crit_chance * 100)}%", font=("Arial", 15), bg='black', fg='red')
crit_text.place(x=310, y=236)

console_text = Text(window, width=40, height=8, bg='black', fg='red', font=("Arial", 11))
console_text.place(x=40, y=370)

# кнопки атаки
mele_attack_button = Button(window, text="melee", bg='black', fg='red', command=lambda: attack("melee"))
mele_attack_button.place(x=40, y=340)

fireball_button = Button(window, text="fireball", bg='black', fg='red', command=lambda: attack("fireball"))
fireball_button.place(x=90, y=340)

iceball_button = Button(window, text="iceball", bg='black', fg='red', command=lambda: attack("iceball"))
iceball_button.place(x=140, y=340)

freeze_button = Button(window, text="freeze", bg='black', fg='red', command=lambda: attack("freeze"))
freeze_button.place(x=190, y=340)

# кнопка побега
escape_button = Button(window, text="escape", bg='black', fg='red', command=escape, )
escape_button.place(x=238, y=340)

# загрузко начального изображения
update_enemy_image()
update_ui()

window.mainloop()