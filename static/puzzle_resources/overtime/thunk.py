# Thunk!
#
# Nathan Pinsker, 3/2017

launch_text = 'You roll your ball into the %s side of the box (i.e., %sward).\n' + \
              'You hear %s thunk%s. The ball pops out on the %s, out of hole %d.\n'

room_text = 'You see a table, a chair, and a door.\n' + \
            'You are holding a wooden ball.\n\n' + \
            'The room is spacious and bright. A box with a large \'#%s\' on it sits on a table.\n'

help_str = 'You find yourself in a mysterious room.\n\n' + \
           'Type \'look\' to look around, or \'look [object]\' to look at an object.\n' + \
           'Type a COMMAND followed by a TARGET to interact with an object in the room.\n'

# answer: 7 / 9
box_text = '''Let's sing the alphabet: A, B, C, D, E...'''

box = ['/L ',
       'L/L',
       'L L']

box_select = [ box ]
signs_text = [ box_text ]

current_index = 0
history = ''
current_box = [k for k in box_select[current_index]]

def pluralize(n):
  return 's' if n != 1 else ''

def direction_to_text(d):
  return {'e': 'east', 'w': 'west', 'n': 'north', 's': 'south', 'north': 'north', 'east': 'east', 'west': 'west', 'south': 'south'}[d]

def direction_to_abbrev(d):
  return {'e': 'e', 'w': 'w', 'n': 'n', 's': 's', 'north': 'n', 'east': 'e', 'west': 'w', 'south': 's'}[d.lower()]

def opposite(d):
  return {'e': 'w', 'w': 'e', 'n': 's', 's': 'n'}[d]

def switch_direction(d):
  return {'/': 'L', 'L': '/', ' ': ' '}[d]

def switch_if(d, if1, if2):
  if d == if1:
    return if2
  elif d == if2:
    return if1
  return d

def increment(x, y, direction):
  if direction == 'n':
    return x, y-1
  elif direction == 's':
    return x, y+1
  elif direction == 'w':
    return x-1, y
  elif direction == 'e':
    return x+1, y
  else:
    return 'Unknown increment %s' % direction

def launch(direction, row, box, should_switch = False):
  d = direction.lower()
  x, y = 0, 0
  w, h = len(box[0]), len(box)
  if d == 'n':
    x, y = row, h - 1
  elif d == 's':
    x, y = row, 0
  elif d == 'w':
    x, y = w - 1, row
  elif d == 'e':
    x, y = 0, row
  else:
    return None, 'What does "%s" mean?\n' % direction, None

  row_options = h
  if d == 'n' or d == 's':
    row_options = w
  if x < 0 or y < 0 or x >= w or y >= h:
    st = 'row' if (d == 'e' or d == 'w') else 'column'
    s = 'You can\'t roll the ball along %s %s, as the box only has %s %ss.\n' % (st, row+1, row_options, st)
    return None, s, None

  mirror_hits = 0

  while x >= 0 and y >= 0 and x < w and y < h:
    current_doodad = box[y][x]
    if current_doodad == '/':
      d = switch_if(d, 'n', 'e')
      d = switch_if(d, 'w', 's')
      mirror_hits += 1
      if should_switch:
        box[y] = box[y][:x] + 'L' + box[y][x+1:]
    elif current_doodad == 'L':
      d = switch_if(d, 'n', 'w')
      d = switch_if(d, 'e', 's')
      mirror_hits += 1
      if should_switch:
        box[y] = box[y][:x] + '/' + box[y][x+1:]
    else:
      pass
    x, y = increment(x, y, d)
  if d == 'e' or d == 'w':
    return d, y, mirror_hits
  return d, x, mirror_hits


def gen_examine_box_str(index, box):
  w = len(box[0])
  h = len(box)
  return ('A mysterious box with a %s pattern on it.\n' + \
         'The box has a large \'#%s\' on the side, and a small placard ' + \
         'underneath with something etched on it.\n' + \
         'The box is %s by %s.\n' + \
         'It has %s holes on each of its west and ' + \
         'east sides (labeled 1 through %s running north to south).\n' + \
         'It has %s holes on each of its north and ' + \
         'south sides (labeled 1 through %s running west to east).\n') % ('torrential',
                                                                           index, w, h, h, h, w, w)

def handle_input(request):
  input_text = request['content']
  hist = request['history']
  global current_index
  global current_box
  global history
  history = hist

  s = input_core(input_text)
  return {'content': s.replace('\n', '[br]'),
          'history': history}


def input_core(input_text):
  global current_index
  global current_box
  global history

  input_text = input_text.split(' ')
  current_box = [k for k in box_select[current_index]]
  if input_text[0] == 'help':
    return help_str
  elif input_text[0] == 'look' or input_text[0] == 'examine' or input_text[0] == 'l' or input_text[0] == 'e':
    if len(input_text) > 1 and (len(input_text) > 2 or input_text[1] != 'around'):
      target = ' '.join(input_text[1:])
      if target == 'box' or target == 'machine' or target == 'thing':
        return gen_examine_box_str(current_index+1, current_box)
      elif target == 'boxes':
        return 'Just one box, labeled #%s, which is on the table.\n' % (current_index+1)
      elif target == 'table':
        return 'The table is made of oak. It stands steadfast and strong.\n'
      elif target == 'door':
        return 'The door doesn\'t look like it can be opened.'
      elif 'sign' in target:
        return 'The elements have worn away at this sign. It\'s too tattered to read.'
      elif target == 'placard':
        return signs_text[current_index] + '\n'
      elif 'ball' in input_text:
        return 'The ball is smooth, polished, and heavy in your hand.\n' + \
              'Roll it into a box by typing "roll [direction] [number]".\n'
      elif target == 'chair':
        return 'Made of wood, but seems a little flimsy.\n'
      elif target == 'table':
        return 'A very high-quality oaken table, about two inches thick and ' + \
              'with four sturdy legs.\n'
      elif target == 'room':
        return room_text % (current_index+1)
      else:
        return 'I don\'t know what you\'re trying to look at.\n'
    else:
      return room_text % (current_index+1)
  elif input_text[0] == 'talk':
    return 'Nobody in this room to talk to but yourself, sport.\n'
  elif input_text[0] == 'fire' or input_text[0] == 'ball' or input_text[0] == 'roll' or input_text[0] == 'launch':
    hist_split = [[history[i], int(history[i+1])] for i in range(0, len(history), 2)]
    for d, r in hist_split:
      launch(d, r, current_box, True)

    if len(input_text) >= 3 and input_text[2].isdigit():
      input_text[1] = direction_to_abbrev(input_text[1])
      d, row, hits = launch(input_text[1], int(input_text[2]) - 1, current_box, True)
      if d:
        s = launch_text % (direction_to_text(opposite(input_text[1])),
                             direction_to_text(input_text[1]),
                             hits, pluralize(hits),
                             direction_to_text(d), row+1)
        history += input_text[1] + str(int(input_text[2])-1)
        return s
      else:
        return row
    elif len(input_text) >= 3 and input_text[1].isdigit():
      # lol
      input_text[2] = direction_to_abbrev(input_text[2])
      d, row, hits = launch(input_text[2], int(input_text[1]) - 1, current_box, True)
      if d:
        s = launch_text % (direction_to_text(opposite(input_text[2])),
                             direction_to_text(input_text[2]), hits, pluralize(hits),
                             direction_to_text(d), row+1)
        history += input_text[2] + str(int(input_text[1])-1)
        return s
      else:
        return row
    else:
      return 'You can\'t roll like that. Try \'roll [direction] [number]\'.\n'
  elif input_text[0] == 'open':
    if input_text[1] == 'door':
      return 'The door is locked.\n'
    else:
      return 'That doesn\'t look like it can be opened.'
  elif input_text[0] == 'take':
    return 'You already have everything you need right now.\n'
  else:
    return 'Sorry, that command doesn\'t work. Type \'help\' for help.\n'

if __name__ == '__main__':
  while True:
    print input_core(raw_input('>> '))
