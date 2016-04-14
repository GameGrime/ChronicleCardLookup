import os, csv, contextlib


def loadCards():
  cardList = []

  with open('cards.csv', 'r', encoding='utf-8-sig') as cardFile:
    cardCSV = csv.DictReader(cardFile, delimiter='\t')
    for card in cardCSV:
      cardList.append(card)

  print('Read cards.csv and loaded %d cards.' % len(cardList))
  return cardList


def loadStrings():
  stringList = []

  with open('loc.csv', 'r', encoding='utf-8-sig') as stringFile:
    stringCSV = csv.DictReader(stringFile, delimiter='\t')
    for string in stringCSV:
      stringList.append({'id':string['id'], 'en':string['en']})

  print('Read loc.csv and loaded %d strings.' % len(stringList))
  return stringList


def getLegend(card):
  arch = card['archetype']
  legendMap = {
    '0': 'All',
    '1': 'Linza',
    '2': 'Raptor',
    '3': 'Ariane',
    '4': 'Ozan',
    '5': 'Vanescula'
  }
  try:
    legend = legendMap[arch]
  except KeyError:
    familyString = ''

  return legend


def getType(card):
  typeNumber = card['type']
  typeMap = {
    '0': 'Other',
    '1': 'Support',
    '2': 'Enemy'
  }
  try:
    typeString = typeMap[typeNumber]
  except KeyError:
    familyString = ''

  return typeString


def getFamily(card):
  familyNumber = card['family']
  familyMap = {
    '': 'None',
    '0': 'None',
    '1': 'Beast',
    '2': 'Demon',
    '3': 'Dragon',
    '4': 'Location',
    '5': 'Equipment',
    '6': 'Familiar',
    '7': 'Giant',
    '8': 'Goblin',
    '9': 'Kalphite',
    '10': 'Ogre',
    '11': 'Ork',
    '12': 'Pirate',
    '13': 'Potion',
    '14': 'Ship',
    '16': 'Spell',
    '17': 'Troll',
    '18': 'Tzhaar',
    '19': 'Tzhaar',
    '20': 'Ally',
    '21': 'Mahjarrat', # Zemouregal and Bilrach - currently disabled/unused
    '22': 'Vampyre',
    '23': 'Action'
  }
  try:
    familyString = familyMap[familyNumber]
  except KeyError:
    familyString = ''

  return familyString


def getReward(card, num):
  reward = ''
  value = ''

  cardRType = card["reward%stype" % num]
  cardRVal1 = card["reward%svalue0" % num]
  cardRVal2 = card["reward%svalue1" % num]

  if cardRType == '2': # Gold
    reward = 'gold'
    value = str(int(cardRVal1)+1)

  elif cardRType == '3': # Health
    reward = 'health'
    value = str(int(cardRVal1)+1)

  elif cardRType == '4': # Base Attack
    reward = 'attack'
    value = str(int(cardRVal1)+1)

  elif cardRType == '5': # Armour
    reward = 'armour'
    value = str(int(cardRVal1)+1)

  elif cardRType == '6': # Weapon
    reward = 'weapon'
    wepAtk = str(int(cardRVal1)+1)
    wepDur = str(int(cardRVal2)+1)
    value  = "%s/%s" % (wepAtk, wepDur)

  else: # Other (Type = 0 usually)
    pass

  return (reward, value)


def getStrings(card, stringList):
  effectID = card['effectdesc']
  if effectID != '':
    effectString = [string['en'] for string in stringList if string['id'] == effectID][0]
  else:
    effectString = ''

  descID = card['descid']
  if descID != '':
    descString = [string['en'] for string in stringList if string['id'] == descID][0]
  else:
    descString = ''

  return (effectString, descString)


def getSource(card):
  sourceNumber = card['source']
  sourceMap = {
    '0': 'Other',
    '1': 'Base',
    '2': 'Leveling',
    '3': 'Packs',
    '4': 'Effects'
  }
  try:
    sourceString = sourceMap[sourceNumber]
  except KeyError:
    sourceString = ''

  return sourceString


def valOrNull(val):
  return (val if val != '' else "null")

#---------------------------------------------------------------------

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

cardList = loadCards()
stringList = loadStrings()

with contextlib.suppress(FileNotFoundError):
  os.remove('cardData.json')

with open('cardData.json', 'w') as cardDataFile:
  cardDataFile.write("[\n")
  counter = 0
  for card in cardList:
    card['legend'] = getLegend(card)
    card['type'] = getType(card)
    card['family'] = getFamily(card)
    (card['reward0type'], card['reward0val']) = getReward(card, '0')
    (card['reward1type'], card['reward1val']) = getReward(card, '1')
    (card['reward2type'], card['reward2val']) = getReward(card, '2')
    (card['effect'], card['desc']) = getStrings(card, stringList)

    cardDataFile.write("  {\n")
    cardDataFile.write("    \"id\":%s,\n" % valOrNull(card['id']))
    cardDataFile.write("    \"name\":\"%s\",\n" % card['name'])
    cardDataFile.write("    \"legend\":\"%s\",\n" % card['legend'])
    cardDataFile.write("    \"type\":\"%s\",\n" % card['type'])
    cardDataFile.write("    \"family\":\"%s\",\n" % card['family'])
    cardDataFile.write("    \"attack\":%s,\n" % valOrNull(card['attack']))
    cardDataFile.write("    \"health\":%s,\n" % valOrNull(card['health']))
    cardDataFile.write("    \"goldcost\":%s,\n" % valOrNull(card['goldcost']))
    cardDataFile.write("    \"r0type\":\"%s\",\n" % card['reward0type'])
    cardDataFile.write("    \"r0val\":\"%s\",\n" % card['reward0val'])
    cardDataFile.write("    \"r1type\":\"%s\",\n" % card['reward1type'])
    cardDataFile.write("    \"r1val\":\"%s\",\n" % card['reward1val'])
    cardDataFile.write("    \"r2type\":\"%s\",\n" % card['reward2type'])
    cardDataFile.write("    \"r2val\":\"%s\",\n" % card['reward2val'])
    cardDataFile.write("    \"rarity\":%s,\n" % valOrNull(card['rarity']))
    cardDataFile.write("    \"effect\":\"%s\",\n" % card['effect'])
    cardDataFile.write("    \"desc\":\"%s\"\n" % card['desc'])
    counter += 1
    if counter < len(cardList):
      cardDataFile.write("  },\n")
    else:
      cardDataFile.write("  }\n")

  cardDataFile.write("]")