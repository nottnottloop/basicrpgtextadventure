import random
import sys
import time
import textwrap
import shutil


# This code allows centered text to print
def centprint(text):
    wrapped_text = textwrap.wrap(text)
    for line in wrapped_text:
        print(line.center(columns))


# This displays stats, probably will use this function a lot
def display_stats(newline=False):
    print('Your stats currently are: Hitpoints: %s, Attack level: %s, Coolness: %s' % (hp, attack, coolness))
    if newline:
        print('')


# This class defines a monster in the game, with HP, an attack stat, name, description and whether it's dead or not
class Monster:
    def __init__(self, mob_hp, mob_attack, mob_name, mob_desc, dead=False, finalboss=False):
        self.hitpoints = mob_hp
        self.attack = mob_attack
        self.mob_name = mob_name
        self.mob_desc = mob_desc
        self.dead = dead
        self.finalboss = finalboss

    def monster_attacks(self):
        global hp
        if debug:
            print('DEBUG: Health before YOU got attacked: ' + str(hp))
        hp -= self.attack
        print('You got HIT for %s hitpoints! @_@\n' % str(current_monster.attack))
        if hp <= 0:
            game_lose()

    def kill(self):
        self.dead = True
        if self.finalboss:
            game_win()


# Initialise game variables
def init_game_vars():
    global hp, attack, coolness, turn_count, action_taken, won, debug, current_monster, current_monster_num, \
        monster_index, numitems, inventory, health_potion, mr_muscles_brew, itemid
    hp = random.randint(5, 10)
    attack = random.randint(5, 10)
    coolness = random.randint(3, 7)
    turn_count = 0
    action_taken = False
    won = False
    debug = False

    # Individual MONSTERS are defined here
    crab = Monster(25, 2, 'a shielded crab with a silly face!', 'Awwww! He\'s got cute little pincers and '
                                                                'an adorable face :)')
    werewolf = Monster(10, 4, 'a horrifying werewolf!', r'Werewolf: "asdfjgkl raaawwww"')
    floating_piece_of_paper = Monster(2, 6, 'OH MY GOSH! A FLOATING SHOPPING LIST! AHHHHHH!!!!!',
                                      r'"MILK, EGGS, CHEESE"')
    big_bad_boss_man = Monster(50, 9, 'the nightmarish final boss without a visual description!',
                               'I guess he looks like Giygas from Earthbound?', finalboss=True)

    # Initialise MONSTER indexing system
    monster_index = [crab, werewolf, floating_piece_of_paper, big_bad_boss_man]
    current_monster_num = 0
    current_monster = monster_index[current_monster_num]

    # ITEMS
    numitems = 0
    inventory = {}
    itemid = {}
    health_potion = Item('heal', 10, 'Health Potion', 'A generic health potion, red and everything. '
                                                      'Labelled with a heart (...is that a'
                                                      ' real human heart instead of a cartoon??)')
    mr_muscles_brew = Item('buff', 4, 'Mr Muscle\'s Brew', 'Mr Muscles\'s Patented Muscle formula!')
    # item3 = Item('buff', 4, 'hmmmmm', 'artsrastrast')


# Initialise the variables only relevant before game starts
columns, rows = shutil.get_terminal_size(fallback=(80, 24))
columns -= 1
welcome_spaces = 80
itemerror = "You didn't pick a valid item. Select an item by entering the number in the square brackets: []"


# This defines an item
class Item:
    def __init__(self, ability, amount, itemname, itemdesc, quant=0):
        global numitems, inventory, itemid
        self.ability = ability
        self.amount = amount
        self.name = itemname
        self.desc = itemdesc
        self.quant = quant
        #self.quant = 2  # quant, was used to bugtest the inventory system in the past
        # Assign a unique ID to each item based on the items that came previously
        # So the health potion should be '0', muscles juice should be '1' etc.
        inventory[numitems] = self
        itemid[numitems] = self
        numitems += 1
        self.itemid = numitems

    def use(self):
        global numitems, action_taken
        if self.quant > 0:
            if self.ability == 'heal':
                heal(self.amount)
            if self.ability == 'buff':
                buff(self.amount)
            action_taken = True
            self.quant -= 1

    def find_item(self):
        self.quant += 1
        print('You found a %s!' % self.name)


def heal(amount):
    global hp
    hp += amount
    print('\nYou were healed for: ' + str(amount))


def buff(amount):
    global attack
    attack += amount
    print('\nSweet! Your attack stat increased by ' + str(amount))


def attackfn():
    global action_taken
    action_taken = True
    current_monster.hitpoints -= attack
    if debug:
        print('DEBUG: Health before attack: ' + str(current_monster.hitpoints))
        print('\nYou struck the monster for %s hitpoints!!\n' % attack)
        print('DEBUG: Health after attack: ' + str(current_monster.hitpoints))
    else:
        print('\nYou struck the monster for %s hitpoints!!\n' % attack)
    if current_monster.hitpoints <= 0:
        current_monster.dead = True
        if current_monster.finalboss:
            game_win()


def act():
    global action_taken
    action_taken = True
    print('\n' + current_monster.mob_desc + '\n')


def item():
    global inventory, itemerror, action_taken

    def print_inv(return_dict=False, return_pos=False):
        menu_position = 0
        menu_pos_to_inventory = {}
        if not return_dict and not return_pos:
            print('\nITEMS: ', end='')
        for i in range(len(inventory)):
            if inventory[i].quant > 0:
                menu_position += 1
                menu_pos_to_inventory[menu_position] = i
                if not return_dict and not return_pos:
                    print(inventory[menu_pos_to_inventory[menu_position]].name + ' [%s]' % str(menu_position), end=': ')
                    print(inventory[menu_pos_to_inventory[menu_position]].quant, end=', ')
        if not return_dict and not return_pos:
            print('\nPick an [item] to use, or [c]ancel:', end=' ')
        if return_pos:
            return menu_position
        else:
            return menu_pos_to_inventory

    print_inv()

    # Data validation to see if user wants to cancel usage of item
    while True:
        itemchoicetext = input()
        if itemchoicetext.startswith('c'):
            break
        try:
            itemchoice = int(itemchoicetext)
        except ValueError:
            print(itemerror)
            continue

        if itemchoice in print_inv(return_dict=True):
            inventory[print_inv(return_dict=True)[itemchoice]].use()
            break
        else:
            print(itemerror)
            print_inv()
    print('')


def mercy():
    global action_taken
    action_taken = True
    print('\nYou pass your turn...\n')


def game_lose():
    print(''.center(columns, '*'))
    centprint('Game Over')
    centprint('...try again? (Y/N)')
    print(''.center(columns, '*'))
    while True:
        try:
            try_again_prompt = input().lower()
        except TypeError:
            print('Invalid input')
            continue
        if try_again_prompt.startswith('y'):
            break
        elif try_again_prompt.startswith('n'):
            print('Okay then, see you around!')
            time.sleep(3.5)
            sys.exit()
        else:
            print('Invalid input')
            continue


def game_win():
    global won, turn_count
    won = True
    print(''.center(columns, '*'))
    centprint('CONGRATULATIONS! YOU HAVE WON! :)')
    centprint('You won in %s turns. ' % turn_count)
    centprint('Thanks for playing and putting up with all that RNG.')
    print(''.center(columns, '*'))
    time.sleep(3.5)
    sys.exit()


# The main function begins from here
print(''.center(columns, '*'))
centprint('Welcome to an intense and basic text based adventure game, with incredibly spooky monsters to fight! >:D')
print(''.center(columns, '*'))

while True:
    # Reset current monster back to the start
    init_game_vars()
    name = input('\nVerily, mighty traveller, what be your name forsooth?\n')
    if name == 'debug':
        print('BEEP BOOP debug mode active, have one of all items too')
        hp, attack, coolness = 999, 999, 999
        debug = True

    else:
        centprint('A fine name, '+name+'!')

    centprint('You start this silly little adventure with completely random stats,'
              ' because I made it that way!')
    print()
    switcher = {'a': attackfn, 'b': act, 'c': item, 'd': mercy}

    # Main game loop begin!
    while hp > 0 and not won:
        action_taken = False
        if current_monster.dead and not current_monster.finalboss:
            # If the current monster dies, be sure to increment the monster count
            current_monster_num += 1
        # Recheck what the current monster is, they could have died the previous turn
        current_monster = monster_index[current_monster_num]

        print('You\'re being attacked by ' + current_monster.mob_name)
        display_stats()
        print('ATTACK (a), ACT (b), ITEM (c), MERCY (d)')
        choice = str(input()).lower()
        if choice in switcher:
            turn_count += 1
            switcher[choice]()
        else:
            print('Invalid input!\n')
            continue
        if action_taken and not current_monster.dead:
            current_monster.monster_attacks()
            if random.randint(1, 10) <= coolness:
                itemid[(random.randint(0, numitems - 1))].find_item()
