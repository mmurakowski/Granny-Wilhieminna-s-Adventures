import sys, random, time, collections, difflib

def clip_clop():
    for item in DATA['INTRO']:
        for line in item.splitlines():
            print(line)
            time.sleep(0.15)
        time.sleep(1.5)
    input("Press ENTER to get started, Granny...")
    print("")
    
    print_output(DATA[STATE.LOCATION], STATE.VERB, STATE.SUBJECT)
    while True:
        verb, subject = get_and_parse_input(DATA[STATE.LOCATION], STATE.INVENTORY)
        location = STATE.LOCATION
        if verb == 'go':
            location = subject
            verb = subject = ''
        if verb == 'examine':
            print_output(DATA, 'ITEMS', ITEMS[subject])
            continue
        item = print_output(DATA[location], verb, subject)
        if item == ITEMS['THE END']:
            sys.exit()
        if verb == 'give':
            STATE.INVENTORY.remove(subject[1])
        if not isinstance(item, str):
            STATE.INVENTORY.append(item)
        if verb == 'take':
            DATA[STATE.LOCATION][verb].pop(subject)
        STATE.LOCATION = location
        STATE.VERB = verb
        STATE.SUBJECT = subject

def print_help(valid_inputs):
    valid_inputs = sorted({i.lower().strip() for i in valid_inputs})
    print('Your options are:\n    {}'.format('   '.join(valid_inputs)))

def get_and_parse_input(options, inventory):
    valid_inputs = {}
    INV_ITEMS = {v:k for k,v in ITEMS.items()}
    for key, values in options.items():
        if not key:
            continue
        if key == 'give':
            for subject, items in values.items():
                for item in set(items) & set(STATE.INVENTORY):
                    valid_inputs['{} {} {}'.format(key, subject, INV_ITEMS[item])] = (key, (subject, item))
            continue
        for value in values:
            valid_inputs['{} {}'.format(key, value)] = (key, value)
    for item in STATE.INVENTORY:
        valid_inputs['examine {}'.format(INV_ITEMS[item])]  = ('examine', INV_ITEMS[item])
    while True:
        print('\nWhat do you want to do next, Granny?')
        original_input_text = input('>>> ')
        input_text = original_input_text.lower().strip()
        if not input_text or 'help' in input_text or '?' in input_text:
            print_help(valid_inputs)
            continue
        matching_inputs = difflib.get_close_matches(input_text, valid_inputs, 1)
        if not matching_inputs:
            error_text = random.choice(DATA['ERRORS']).format(original_input_text)
            print(error_text)
            print_help(valid_inputs)
        else:
            return valid_inputs[matching_inputs[0]]

def print_output(options, verb, subject):
    if verb == 'give':
        text = options[verb][subject[0]][subject[1]]
    else:
        text = options[verb][subject]
    for line in text:
        if isinstance(line, str):
            input(line)
    return line

'''
  ██████  ██▓███   ▒█████   ██▓ ██▓    ▓█████  ██▀███    ██████ 
▒██    ▒ ▓██░  ██▒▒██▒  ██▒▓██▒▓██▒    ▓█   ▀ ▓██ ▒ ██▒▒██    ▒ 
░ ▓██▄   ▓██░ ██▓▒▒██░  ██▒▒██▒▒██░    ▒███   ▓██ ░▄█ ▒░ ▓██▄   
  ▒   ██▒▒██▄█▓▒ ▒▒██   ██░░██░▒██░    ▒▓█  ▄ ▒██▀▀█▄    ▒   ██▒
▒██████▒▒▒██▒ ░  ░░ ████▓▒░░██░░██████▒░▒████▒░██▓ ▒██▒▒██████▒▒
▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░░ ▒░▒░▒░ ░▓  ░ ▒░▓  ░░░ ▒░ ░░ ▒▓ ░▒▓░▒ ▒▓▒ ▒ ░
░ ░▒  ░ ░░▒ ░       ░ ▒ ▒░  ▒ ░░ ░ ▒  ░ ░ ░  ░  ░▒ ░ ▒░░ ░▒  ░ ░
░  ░  ░  ░░       ░ ░ ░ ▒   ▒ ░  ░ ░      ░     ░░   ░ ░  ░  ░  
      ░               ░ ░   ░      ░  ░   ░  ░   ░           ░  
                                                                
             ▄▄▄▄   ▓█████  ██▓     ▒█████   █     █░           
            ▓█████▄ ▓█   ▀ ▓██▒    ▒██▒  ██▒▓█░ █ ░█░           
            ▒██▒ ▄██▒███   ▒██░    ▒██░  ██▒▒█░ █ ░█            
            ▒██░█▀  ▒▓█  ▄ ▒██░    ▒██   ██░░█░ █ ░█            
            ░▓█  ▀█▓░▒████▒░██████▒░ ████▓▒░░░██▒██▓            
            ░▒▓███▀▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▒░▒░ ░ ▓░▒ ▒             
            ▒░▒   ░  ░ ░  ░░ ░ ▒  ░  ░ ▒ ▒░   ▒ ░ ░             
             ░    ░    ░     ░ ░   ░ ░ ░ ▒    ░   ░             
             ░         ░  ░    ░  ░    ░ ░      ░               
                  ░                                             

You can peek behind the curtain, but you might not like what you find.
'''

class STATE:
    LOCATION = 'outside'
    VERB = ''
    SUBJECT = ''
    INVENTORY = []

ITEMS = collections.defaultdict(lambda : object())

DATA = {
    'INTRO': [
        '''
     ________                                      __      __.__.__  .__    .__               .__                          
    /  _____/___________    ____   ____ ___.__.   /  \    /  \__|  | |  |__ |__| ____   _____ |__| ____   ____ _____       
   /   \  __\_  __ \__  \  /    \ /    <   |  |   \   \/\/   /  |  | |  |  \|  |/ __ \ /     \|  |/    \ /    \\__  \      
   \    \_\  \  | \// __ \|   |  \   |  \___  |    \        /|  |  |_|   Y  \  \  ___/|  Y Y  \  |   |  \   |  \/ __ \_    
    \______  /__|  (____  /___|  /___|  / ____|     \__/\  / |__|____/___|  /__|\___  >__|_|  /__|___|  /___|  (____  /    
           \/           \/     \/     \/\/               \/               \/        \/      \/        \/     \/     \/     

                                                        .__                                                                
                                                        |__| ____                                                          
                                                        |  |/    \                                                         
                                                        |  |   |  \                                                        
                                                        |__|___|  /                                                        
                                                                \/                                                         

  ________                                      __      __.__.__  .__    .__               .__                  /\         
 /  _____/___________    ____   ____ ___.__.   /  \    /  \__|  | |  |__ |__| ____   _____ |__| ____   ____ ____)/   ______
/   \  __\_  __ \__  \  /    \ /    <   |  |   \   \/\/   /  |  | |  |  \|  |/ __ \ /     \|  |/    \ /    \\__  \  /  ___/
\    \_\  \  | \// __ \|   |  \   |  \___  |    \        /|  |  |_|   Y  \  \  ___/|  Y Y  \  |   |  \   |  \/ __ \_\___ \ 
 \______  /__|  (____  /___|  /___|  / ____|     \__/\  / |__|____/___|  /__|\___  >__|_|  /__|___|  /___|  (____  /____  >
        \/           \/     \/     \/\/               \/               \/        \/      \/        \/     \/     \/     \/ 
     __________                           .________      _____       .___                    __                            
     \______   \_____    ____   ____      |   ____/     /  _  \    __| _/__  __ ____   _____/  |_ __ _________   ____      
      |    |  _/\__  \  /    \_/ __ \     |____  \     /  /_\  \  / __ |\  \/ // __ \ /    \   __\  |  \_  __ \_/ __ \     
      |    |   \ / __ \|   |  \  ___/     /       \   /    |    \/ /_/ | \   /\  ___/|   |  \  | |  |  /|  | \/\  ___/     
      |______  /(____  /___|  /\___  >   /______  /   \____|__  /\____ |  \_/  \___  >___|  /__| |____/ |__|    \___  >    
             \/      \/     \/     \/           \/            \/      \/           \/     \/                        \/     

                   ________ ________________________.___.     ___________    .___.__  __  .__                              
                  /  _____/ \_____  \__    ___/\__  |   |     \_   _____/  __| _/|__|/  |_|__| ____   ____                 
                 /   \  ___  /   |   \|    |    /   |   |      |    __)_  / __ | |  \   __\  |/  _ \ /    \                
                 \    \_\  \/    |    \    |    \____   |      |        \/ /_/ | |  ||  | |  (  <_> )   |  \               
                  \______  /\_______  /____|    / ______|     /_______  /\____ | |__||__| |__|\____/|___|  /               
                         \/         \/          \/                    \/      \/                         \/                
''', '''
                               _______    __              _____                            __  
                              / / ____|  / _|            / ____|                           \ \ 
                             | | |  __  | |_ ___  _ __  | |  __ _ __ __ _ _ __  _ __  _   _ | |
                             | | | |_ | |  _/ _ \| '__| | | |_ | '__/ _` | '_ \| '_ \| | | || |
                             | | |__| | | || (_) | |    | |__| | | | (_| | | | | | | | |_| || |
                             | |\_____| |_| \___/|_|     \_____|_|  \__,_|_| |_|_| |_|\__, || |
                              \_\                                                      __/ /_/ 
                                                                                      |___/    
''',
        'Welcome to the world of the West Marches.',
        "In this game you take on the role of everyone's favorite venerable old horse, Granny Wilhieminna.",
        'Type the actions you wish to perform and press ENTER',
        'At any time you can type ? to bring up your options.'],
    'ERRORS': [
        "You must be getting senile. There's no way you could {}.",
        'Granny, old girl, you must have had too much to drink if you think you can {}.',
        "You can't {} right now. Maybe later.",
        'Your grandchildren never visit anymore, maybe because you keep trying to {}',
        "Back in your day, you'd {} uphill, in the snow. Children these days don't know how good they've got it.",
        'Once, when you were a young girl, your parents took you into town to {}; ah, this takes you back...',
        "You shouldn't waste time trying to {} when you've got so many horses to abuse.",
        "Granny, old girl, now's not the time to be trying to {}.",
        "You only have a few years left on this earth, you shouldn't waste them trying to {}.",
        "Now what'd make you think you could {}?",
        "Trying to {} is hardly appropriate for a woman your age.",
    ],
    'ITEMS': {
        ITEMS['stairs']: ['The stairs are extremely heavy but your new horse form is strong.',
                          'Is carrying them a problem?',
                          'Nay!'],
        ITEMS['brush']: ["A coarse-haired brush, perfect for your thick coat.",
                         "You just need to find someone to help you use it."],
        ITEMS['stock']: ["Some stock. You reflect upon it for a minute."],
        ITEMS['sock']: ["You don't want to think about the light magics permeating it."],
    },
    'hallway': {
        '': {'': ['The ENTRY HALL of the BANDITBANE MANOR is sparsely decorated.',
                  'A coat rack stands by the door.',
                  "You're dripping wet and want to find someone to help dry you off."]},
        'go': ['outside', 'your room', 'kitchen', "percival's room", "weskin's room"],
        'look': {
            'around': ['You stand in the entryway of the BANDITBANE MANOR.',
                      'Behind you is the door to the OUTSIDE; brr!',
                      'Down the hall to your left is the KITCHEN.',
                      "To your right is the door to PERCIVAL'S ROOM.",
                      "Up the STAIRS is YOUR ROOM and WESKIN's ROOM."],
        },
        'talk': {
            'self': ['Look at the state of this place! It looks like a bunch of transient vagrants live here!',
                     "Well, a grandmother's touch should fix that right up.",
                     "But you've got to stay focused, Granny, old girl."],
        },
        'take': {
            'stairs': ['You take the stairs.',
                       ITEMS['stairs']],
        },
    },
    'kitchen': {
        '': {'': ['You enter the KITCHEN.',
                  'The two halflings LEOPOLD and MEERA sitting at a wooden table, with bowls of STEW in front of them.',
                   'A pot bubbles on the hearth. It smells delicious.']},
        'go': ['hallway'],
        'look': {
            'around': ['This kitchen looks less well-used than your old one.',
                       'You suppose that nobody here really has time to cook, what with being out and about all the time.',
                       "No, no, it's fine, leave your poor old grandmother here to do the cooking while you go on your adventures."],
            'leopold': ["This is the first time you've seen Leopold outside his room.",
                        "Whatever happened to him, it looks like he's gotten over it."],
            'meera': ["She's certainly looking better since her last encounter with Malika.",
                      "Rest and a hearty meal has restored her spirits, as you knew it would."],
            'stew': ['A tasty-looking pot of thick brown stew bubbles on the hearth.',
                     'There is something enticingly other-worldly about it.',
                     'It looks like the halflings have been eating it for most of the morning.'],
        },
        'take': {
            'stew': ['The halflings regard you with undisguised loathing as you dig in to their brunch.',
                     'Whippersnappers need to learn to respect their elders.',
                     "If you'd been forty years younger, you'd have half a mind to tan their hides.",
                     '...',
                     'You finish your meal.',
                     'Delicious.'],
            'stew ': ['The halflings regard you with undisguised wonder as you continue eating.',
                      "It's no wonder hobbits get so fat, eating food this good.",
                      'You ladle yourself a second bowl, and lick it clean, then go back for a third helping.',
                      'Delicious.',
                      'But not quite as filling as you had hoped.',
                      'More. You want more.'],
            'stew  ': ['The halflings regard you with undisguised terror as you continue eating.',
                       'You shovel stew into your gluttonous maw, barely pausing to breathe.',
                       'Your vision tunnels and all you can see is the pot and the life-giving broth contained within.',
                       'MORE.',
                       'MUST EAT MORE.',
                       'The stew is gone but your endless insatiable hunger still remains.',
                       'There is no more Wilhieminna left, there is only that single ravenous need.',
                       "A sound like a whimper escapes Meera's lips.",
                       'You drop your spoon with a clatter and look at her with hunger in your eyes.',
                       'THE END',
                       ITEMS['THE END']],
        },
        'talk': {
            'leopold': ['Leopold looks blankly at you as you expound on the virtues of light eating.',
                        'He nods, and returns to his meal.'],
            'meera': ['''"Hello, Meera! I'm glad to see you're doing better."''',
                      '"Thank you, Granny."',
                      '"Could I trouble you to help me brush my mane?"',
                      '''"I would be more than happy to, Granny, but I'm busy right now," she says, indicating her bowl.''',
                      '''"Besides," she continues, "I don't have a brush with me."''',
                      "Perhaps, old girl, you'd better get her a brush."],
            'self': ["Granny, old girl, these banditbaners don't know the first thing about keeping a kitchen.",
                     "You've got to show them how it's done some time."],
        },
        'give': {
            'leopold': {
                ITEMS['brush']: ["After some cajoling, you convince Leopold to interrupt his meal to take care of his poor old grandmother.",
                                 "He grips the brush and swings it wildly before bringing it down on your exposed flank.",
                                 "You neigh in pain and surprise.",
                                 "Now you're damp *and* bruised. Great.",
                                 ITEMS['brush']],
            },
            'meera': {
                ITEMS['brush']: ['"Meera, I have brought you a brush," you say, holding the brush out to her.',
                                 '"Now, can you help your poor old grandmother with a brushing?"',
                                 '"Of course," she says, taking it from you gingerly',
                                 'She is a good girl, so polite and willing to help.',
                                 'You lose yourself in the feeling of being taken care of.',
                                 '''Once she finishes, Meera says, "Grandmother, I have something special; I'll be back soon."''',
                                 'Leopold continues to inore you, concentrating on his stew, as Meera leaves the kitchen.',
                                 'Shortly, Meera returns, carrying a bundle of broad colorful ribbons.',
                                 'She spends the three hours carefully braiding them into your mane and tail.',
                                 'This was a good day.',
                                 'THE END',
                                 ITEMS['THE END']],
                ITEMS['stock']: ['She regards your gift for a moment before smiling.',
                                 '"Thank you, Granny, our pot was running low."'],
            }
        },
    },
    'outside': {
        '': {'': ['You are OUTSIDE the BANDITBANE MANOR.',
                  'It is a cold Bane 5 morning; sleet is falling and soaking you.',
                  'Better get inside quickly, before you catch cold.']},
        'go': ['stable', 'inside', 'gardholme'],
        'look': {
            'around': ['In your immediate are is the STABLE and the BANDITBANE MANOR.',
                       'GARDHOLME stretches out around you, and beyond it the wild WEST MARCHES'],
            'gardholme': ['The city of Gardholme stretches out around you.',
                         'It looks to be shuttered up against the weather with only a few brave souls venturing out into the sleet.',
                         "You hope they don't catch cold."],
            'manor': ["Your new adopted family the BANDITBANERS live inside.",
                      "You suppose you'll remain here for the forseeable future."],
            'stable': ["The stable is a low thatch-roofed building that houses the Banditbaners' HORSES and DOGS.",
                       'Those brave animals work without complaint.',
                       'You think ELLAMIR is inside.'],
        },
        'talk': {
            'self': ["Granny, old girl, you're going to make yourself sick standing out here."]
        },
        'take': {
            'stock': ['You take stock of your situation.',
                      'You are a frail old woman that has recently come into a horse body and found a new family.',
                      "But you're standing in the cold sleet, freezing to death.",
                      "You should get inside and find someone to help you dry off and brush your coat.",
                      ITEMS['stock']],
        },
    },
    'gardholme': {
        '': {'': ["You set off in a random direction into the city.",
                  "Few people are out in this weather, but those that are shy away from you.",
                  "You are unlikely to find anyone to braid your mane out here.",
                  "You're getting more soaked by the second."]},
        'go': ['banditbane manor', "jacobi's shop", "outside the city"]
    },
    "jacobi's shop": {
        '': {'': ["Finally you arrive at a place you know: the shop of Jacobi, the local antiquities dealer.",
                  "The door is closed against the autumn chill.",
                  'A sign hanging on it says "No horses allowed".']},
        'go': ['banditbane manor', 'gardholme', 'outside the city'],
        'take': {
            'a hint': ["Well, you know when you're not welcome somewhere!"]
        },
    },
    'outside the city': {
        '': {'': ["A surly guardsman gazes at you warily before letting you out through the North Gate.",
                  "The walls of the city stretch out behind you, while ahead is largely untamed wilderness.",
                  "A PEANUT SHAPED ROCK is visible in the distance."]},
        'go': ['back east', 'into the city']
    },
    'back east': {
        '': {'': ["Why are you even in Gardholme anymore?",
                  "The beast you chased here is dead and likely to stay that way.",
                  "Your real family misses you.",
                  "And nobody in this blasted town wants to brush your coat.",
                  "You shrug all four shoulders, and without a glance backwards, gallop down the road back home.",
                  "THE END",
                  ITEMS['THE END']]},
    },
    "percival's room": {
        '': {'': ["You barge into Percival's room without knocking.",
                  'PERCIVAL is sitting at his desk; he bolts upright as you enter, and looks sheepish as he rearranges his robes.',
                  '"Yes, grandmother?" he asks.']},
        'go': ['hallway'],
        'look': {
            'around': ["PERCIVAL'S ROOM is a combination bedroom and workshop.",
                       'PERCIVAL is staring at you expectantly.',
                       'A single DISCARDED SOCK lies on the floor, crusted with magic.'],
            'discarded sock': ["A solitary sock befouled during Percival's combat with a ranking clergyman.",
                               "You'd rather not examine it further."],
            'percival': ["He's such a polite young man, and so handsome too.",
                         "You just wish he'd get his head out of the clouds, stop polishing his wand, and get out there and make you some great-grandhorses!"],
        },
        'take': {
            'discarded sock': ['You pick up the sock.',
                               'Ugh, you can smell the magic from here.',
                               ITEMS['sock']]
        },
        'talk': {
            'percival': ['"Percival! Stop polishing your wand for five minutes, I have something important to tell you!"',
                         '"Yes, grandmother, what is it?"',
                         'You spend twenty eight minutes imparting the wisdom of ages to the young Percival.',
                         'He nods and thanks you for the lesson.',
                         "You feel you've done great work this day."],
            'self': ["Granny, old girl, here's a young man that could benefit from your experience.",
                     "If only you had time to take on another apprentice..."],
        },
        'give': {
            'percival': {
                ITEMS['brush']: ['You hold out the brush to Percival.',
                                 '''"You've been sitting in your room long enough! It's time to fulfill your filial duties!"''',
                                 'He tries to wave you away but you stamp your hooves and nibble his hair insistently.',
                                 'Finally, with a sigh, he stands and takes the brush from you.',
                                 'He gets to work, brushing the water from you and smoothing down your cowlicks.',
                                 'His hands are inexpert but, to his credit, he takes direction well.',
                                 'It is not long before you are dry and groomed.',
                                 '"Thank you for taking care of your poor old grandmother," you say.',
                                 'He grumbles something about needing to get back to work.',
                                 '... but something in his eyes tells you he enjoyed it too.',
                                 "Perhaps you'll do this again soon, but meanwhile you've a letter to write.",
                                 'THE END... for now.',
                                 ITEMS['THE END']],
                ITEMS['sock']: ['"Percival, I found one of your experiments," you say, tossing the sock at him.',
                                'He flinches and looks abashed.',
                                '"Sorry, grandmother."'],
            },
        },
    },
    'stable': {
        '': {'': ['You go into the STABLE. It is warm despite the chill, and smells faintly of HORSE manure.',
                  'SMELODY barks at you from the corner and ELLAMIR shushes her.']},
        'go': ['outside'],
        'look': {
            'around': ['A HORSE munches on some feed in a stall.',
                       'ELLAMIR is playing in the corner with his wolf, SMELODY.'],
            'ellamir': ["He's really let himself go since his girlfriend broke up with him.",
                        'You hope he shapes up soon; you want more great-grandwolves!'],
            'horse': ['Faithful steed by day, filling meal by night.',
                      'It gazes at you with sad eyes as though it knows its eventual fate.'],
            'smelody': ["Ellamir is trying to teach it to catch treats out of the air; he's not having much luck.",
                        'This might be because it is A LITERAL WOLF.'],
        },
        'take': {
            'brush': ['You pick up the brush.',
                      'This will come in handy.',
                      ITEMS['brush']]
        },
        'talk': {
            'ellamir': ['"Ellamir! Come and brush your granny\'s coat!"',
                        'He looks back at you blankly.',
                        'Not the smartest boy, is he?',
                        "Still, brains aren't everything and he has such pretty eyes."],
            'horse': ['Neigh!',
                      '*tosses head* Neigh!'],
            'self': ["Granny, old girl, it feels good to be among your kin, doesn't it?",
                     'Maybe you should grab that brush and find someone to use it.'],
            'smelody': ['"Who\'s a good doggie? You are!"',
                        '"WOOF!"'],
        },
        'give': {
            'ellamir': {
                ITEMS['brush']: ["You think Ellamir probably has experience working with animals.",
                                 "Having, you know, dated a druid.",
                                 "You wave the brush in front of his uncomprehending face.",
                                 "Finally, he realizes what you want.",
                                 "He nods and commands Smelody to sit, then takes the brush from your hand.",
                                 "He begins brushing at your shoulder and...",
                                 "Wow.",
                                 "Oh, she must have taught him THAT move.",
                                 "If you ever meet her you'll need to thuuungh",
                                 "mmmmm",
                                 "Ah! Ooooooh.",
                                 "The other horse gazes at you with what you can only imagine is jealousy as Ellamir continues his work.",
                                 "THE END...",
                                 "... for now...",
                                 ITEMS['THE END']],
            },
            'smelody': {
                ITEMS['brush']: ["You hold the brush out to Ellamir's dog.",
                                 '"Woof! Grrrr woof woof woof!"',
                                 "Suddenly Smelody snatches the brush from your hand and bolts out the stable door.",
                                 "You stare after her for a long minute.",
                                 '''"She's probably going to bury it somewhere," says Ellamir.''',
                                 '''"I've been trying to train her to not do that but it's no use," he continues, shaking his head.''',
                                 "In retrospect you're not sure what you were expecting, but it looks like you'll never get your coat taken care of now.",
                                 "THE END",
                                 ITEMS['THE END']],
            },
        },
    },
    "weskin's room": {
        '': {'': ["WESKIN'S ROOM is sparse and spartan.",
                  "A thin mat is rolled out on the floor; WESKIN sits cross-legged in the middle of it, eyes closed.",
                  "He does not react as you enter."]},
        'go': ['hallway'],
        'look': {
            'around': ["There's really not much to see here; WESKIN lives simply, as a monk should."],
            'weskin': ['WESKIN sits cross-legged, with his eyes closed, on a grass mat.',
                       'He breathes steadily and is absolutely still.',
                       'You can see his bulging thighs and lean chest muscles through gaps in his robe.',
                       'Your breath catches slightly and you feel yourself flush under your horse.'],
        },
        'talk': {
            'self': ["Granny, old girl, you're eighty years old.",
                     "Old enough to be his great-grandmother.",
                     "But *look* at those thighs.",
                     "..."],
            'weskin': ["You open your mouth to deliver a lecture on the merits of prune juice but something stops you.",
                       "You feel that any knowledge you could impart has already been mastered by the wise beautiful creature sitting before you.",
                       "Indeed, it is you who should be taking lessons from this Buddha of Love."],
        },
        'give': {
            'weskin': {
                ITEMS['brush']: ['He looks so peaceful in his meditation you almost feel guilty for disturbing him.',
                                 '"Weskin, dear, would you mind helping your granny brush her mane?"',
                                 'He opens his eyes slowly and looks up at you.',
                                 '"Not at all, Grandmother."',
                                 'He stands and takes the brush from you and oh Calistria those hands, to feel them running over your hide...',
                                 'You settle down on his grass mat and he stands over you in a horse stance and those beautiful thighs touch your sides and he gets to work.',
                                 'It is all you can do to keep from moaning as you melt under his gentle care.',
                                 "You don't want to but you can't help...",
                                 'but fall...',
                                 'asleep...',
                                 '...',
                                 'zzzzzz',
                                 'THE END (for now)',
                                 ITEMS['THE END']],
            },
        },
    },
    'your room': {
        '': {'': ['You enter YOUR ROOM.',
                  'A simple BED occupies a corner, with a DESK next to it.',
                  'A tall MIRROR hangs on the wall.']},
        'go': ['hallway'],
        'look': {
            'around': ["It was very kind of the BANDITBANERS to take in their poor old grandmother.",
                       "You've got a few portraits of your great-grandkittens that you ought to put up."],
            'bed': ["The day's too young for sleeping, you silly old bat!"],
            'desk': ['The letter you are composing to your grandcat is laying there, waiting for you to finish it.',
                     'Perhaps later.'],
            'mirror': ["You look at yourself in the mirror.",
                       "Though you're slightly bedraggled and still dripping wet, you can't help but think that your horse form suits you.",
                       "Granny Wilhieminna, you sly old girl, you've never looked better."],
        },
        'talk': {
            'self': ["You're settling in quite nicely, aren't you?",
                     'This is almost starting to feel like home.'],
        },
        'give': {
            'self': {
                ITEMS['brush']: ["You get to work on your horsecoat.",
                                 "It feels good to brush out the water clinging to your flanks.",
                                 "You sigh contentedly as your hands run up and down your sides.",
                                 "Oh no.",
                                 "Your arms aren't long enough to reach your rump.",
                                 "You can't just leave your tail in this sad state.",
                                 "Looks like you'll have to find someone else to help you.",
                                 "Shouldn't be a problem for a majestic beast like yourself.",
                                 ITEMS['brush']],
            },
        },
    }
}
DATA['inside'] = DATA['hallway']
DATA['banditbane manor'] = DATA['outside']
DATA['into the city'] = DATA['gardholme']

if __name__ == '__main__':
    clip_clop()
