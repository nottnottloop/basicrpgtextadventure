import random
import sys
import time
import textwrap
import shutil

# Initialise the variables only relevant before game starts
columns, rows = shutil.get_terminal_size(fallback=(80, 24))
columns -= 0
version = '1.1.3'
# Items are mostly static, inventory is reset in init_game_vars
inventory = {}
numitems = 0
itemerror = "You didn't pick a valid item. Select an item by entering the number in the square brackets: []"
itemid = {}
playing = False

# This code allows centered text to print
def centprint(text):
    wrapped_text = textwrap.wrap(text)
    for line in wrapped_text:
        print(line.center(columns))
    #for line in text:
    #    wrapped_text = textwrap.wrap(text)
    #    print(wrapped_text)

# This displays stats, probably will use this function a lot
def display_stats(newline=False):
    centprint('YOU HAVE: Hitpoints: %s, Attack: %s, Coolness: %s' % (hp, attack, coolness))
    if newline:
        print('')

# This class defines a monster in the game, with HP, an attack stat, name, description and whether it's dead or not
class Monster:
    def __init__(self, mob_hp, mob_attack, mob_name, mob_desc, acttext, shortname, dead=False, finalboss=False):
        self.hitpoints = mob_hp
        self.attack = mob_attack
        self.mob_name = mob_name
        self.mob_desc = mob_desc
        self.dead = dead
        self.finalboss = finalboss
        self.acttext = acttext
        self.shortname = shortname

    def monster_attacks(self):
        global hp
        if debug:
            print('DEBUG: Health before YOU got attacked: ' + str(hp))
        hp -= self.attack
        print()
        centprint('*** The %s HIT you for %s hitpoints! @_@ ***' %
                  (current_monster.shortname, str(current_monster.attack)))
        print()

def kill(self):
    self.dead = True
    if self.finalboss:
        game_win()

def heal(amount):
    global hp
    hp += amount
    print('\n\nYou were healed for: ' + str(amount))

def coolup(amount):
    global coolness
    coolness += amount
    print('\n\nRadical! Your coolness stat increased by ' + str(amount) + '! (This increases your item drop chance)')

def buff(amount):
    global attack
    attack += amount
    print('\n\nSweet! Your attack stat increased by ' + str(amount))

# Define what an item is
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
        global numitems, action_taken, turn_count
        if self.quant > 0:
            if self.ability == 'heal':
                heal(self.amount)
            if self.ability == 'buff':
                buff(self.amount)
            if self.ability == 'coolup':
                coolup(self.amount)
            action_taken = True
            turn_count += 1
            self.quant -= 1

    def find_item(self):
        self.quant += 1
        print('You found a %s!\n' % self.name)

    # When the game variables were getting initialsed the inventory system was getting trashed
    # This is now ran on game init to prevent this
    #def repopulate_inventory(self):
    #    for i in range(numitems):
    #        self = inventory[itemid]

# Define item types
health_potion = Item('heal', 10, 'Health Potion', 'A generic health potion, red and everything. '
                                                  'Labelled with a heart (...is that a'
                                                  ' real human heart instead of a cartoon??)')
mr_muscles_brew = Item('buff', 4, 'Mr Muscle\'s Brew', 'Mr Muscles\'s Patented Muscle formula!')
# item3 = Item('buff', 4, 'hmmmmm', 'artsrastrast')
cool_man_tonic = Item('coolup', 1, 'Cool Dude\'s Tonic', 'Only for the coolest around 8)')


# Initialise game variables
def init_game_vars():
    global hp, attack, coolness, turn_count, action_taken, won, debug, current_monster, current_monster_num, \
        monster_index, inventory, turn_count
    hp = random.randint(5, 10)
    attack = random.randint(5, 10)
    coolness = random.randint(3, 7)
    turn_count = 0
    action_taken = False
    won = False
    debug = False

    # Individual MONSTERS are defined here
    crab = Monster(25, 2, 'a shielded crab with a silly face!',
                          'Awwww! He\'s got cute little pincers and an adorable face :)',
                          'You attempt to distract the shielded menace by striking a pose!',
                          'Crab')
    vampire = Monster(30, 4, 'a horrifying vampire!', r'Vampire: "asdfjgkl raaawwww"',
                             'You wave garlic around in a menacing way!',
                             'Vampire')
    floating_piece_of_paper = Monster(15, 6, 'OH MY GOSH! A FLOATING SHOPPING LIST! AHHHHHH!!!!!',
                                      r'"MILK, EGGS, CHEESE"',
                                      'You slowly erase some of the characters on the list...',
                                      'Shopping List')
    big_bad_boss_man = Monster(100, 7, 'the nightmarish final boss without a visual description!',
                               'I guess he looks like Giygas from Earthbound?',
                               'You do a thing!',
                               'Shambling Horror', finalboss=True)

    # Initialise MONSTER indexing system
    monster_index = [crab, vampire, floating_piece_of_paper, big_bad_boss_man]
    current_monster_num = 0
    current_monster = monster_index[current_monster_num]


def attackfn():
    global action_taken, turn_count

    def strike():
        centprint('* You STRUCK the %s for %s hitpoints!! *' % (current_monster.shortname, attack))

    action_taken = True
    turn_count += 1
    current_monster.hitpoints -= attack
    if debug:
        print('DEBUG: Health before attack: ' + str(current_monster.hitpoints))
        strike()
        print('DEBUG: Health after attack: ' + str(current_monster.hitpoints))
    else:
        print()
        strike()
        print()
    if current_monster.hitpoints <= 0:
        current_monster.dead = True
        if current_monster.finalboss:
            game_win()


def act():
    global action_taken, turn_count, hp
    action_taken = True
    turn_count += 1
    print()
    centprint(current_monster.mob_desc)
    print()
    centprint(current_monster.acttext)
    print('\n')
    if random.randint(0, 1) == 1:
        current_monster.attack -= 2
        if current_monster.attack < 0:
            current_monster.attack = 0
        centprint('You attempt to subdue the ' + current_monster.shortname + ' worked! Its attack was lowered!')
    else:
        centprint('Your attempt to subdue the monster failed...')
        recoil_chance = random.randint(1, 100)
        if recoil_chance <= 5:
            hp -= 99999
            centprint('***OUCH***! I think you just died? How unlucky...')
        elif recoil_chance <= 50:
            hp -= 2
            centprint('You hurt yourself in your confusion!')


def item():
    global inventory, itemerror, action_taken, turn_count

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
    global action_taken, turn_count
    turn_count += 1
    action_taken = True
    print('\nYou pass your turn...\n')

def game_lose():
    global playing
    playing = False
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
    global won, turn_count, playing
    won = True
    playing = False
    print(''.center(columns, '*'))
    centprint('CONGRATULATIONS! YOU HAVE WON! :)')
    centprint('You won in %s turns. ' % turn_count)
    centprint('Thanks for playing and putting up with all that RNG.')
    print(''.center(columns, '*'))
    time.sleep(3.5)
    sys.exit()

def debug_mode():
    global hp, attack, coolness, debug
    print('BEEP BOOP debug mode active, have one of all items too')
    hp, attack, coolness = 999, 999, 999
    for i in range(numitems):
        inventory[i].find_item()
    debug = True

# The main function begins from here
print(''.center(columns, '*'), end='')
#centprint('Welcome to version %s of an intense and basic text based adventure game, '
#          'with incredibly spooky monsters to fight! >:D' % version)
print(r'''  
|_  _. _o _._._  __|_ _  _|_ _. _|   _ .__|_   .__  ._   
|_)(_|_>|(_| |_)(_||_(/_><|_(_|(_|\/(/_| ||_|_||(/_o|_)\/
             |   _|                                 |  / ''')
print(('basicrpgtextadventure.py v%s' % version).rjust(columns))
print(''.center(columns, '*'), end='')

while True:
    # Reset current monster back to the start
    init_game_vars()
    name = input('\nVerily, mighty traveller, what be your name forsooth?\n')
    if name == 'debug':
        debug_mode()
    else:
        centprint('A fine name, '+name+'!')

    centprint('You start this silly little adventure with completely random stats,'
              ' because I made it that way!')
    print()
    switcher = {'a': attackfn, 'b': act, 'c': item, 'd': mercy}
    playing = True

    # Main game loop begin!
    while playing and not won:
        action_taken = False
        if current_monster.dead and not current_monster.finalboss:
            # If the current monster dies, be sure to increment the monster count
            current_monster_num += 1
        # Recheck what the current monster is, they could have died the previous turn
        current_monster = monster_index[current_monster_num]
        if hp <= 0:
            game_lose()
            break

        centprint('You\'re being attacked by ' + current_monster.mob_name)
        display_stats()
        centprint('ATTACK (a), ACT (b), ITEM (c), MERCY (d)')
        choice = str(input()).lower()
        if choice in switcher:
            switcher[choice]()
        else:
            print('Invalid input!\n')
            continue
        if action_taken and not current_monster.dead:
            current_monster.monster_attacks()
            if random.randint(1, 15) <= coolness and hp > 0:
                itemid[(random.randint(0, numitems - 1))].find_item()
