function random_choice(myArray) {
  return myArray[Math.floor(Math.random() * myArray.length)];
}

function generateLootbox() {
  level_table = [0, 8, 22, 36, 44, 58, 72, 80, 80, 80, 80, 88, 97, 107, 118, 130, 143, 157, 157, 157, 157, 171, 185, 193, 201, 209, 217, 225, 225,
                   225, 225, 239, 253, 261, 269, 277, 285, 293, 293, 293, 293, 295, 297, 299, 301, 303, 317, 331, 331, 331, 331, 345, 347, 349, 363, 365, 367];
  level = 0
  seed = Math.random() * 381;
  for (var e = 0; e < level_table.length; e++) {
    if (seed > level_table[e])
        level += 1
  }
  attribute1 = random_choice(["diligent", "belligerent", "eligible", "intelligent", "slight", "profligate", "malignant", "negligible", "religious", "delightful", "obligatory", "negligent", "aligned", "lightweight", "enlightened", "flighty", "light",
                                "prodigal", "gigantic", "navigator’s", "indefatigable", "alligator", "navigational", "Michigan", "investigator’s", "brigand’s", "mitigating", "fumigating",
                                "organic", "arrogant", "elegant", "pagan", "extravagant", "gargantuan", "organized", "Ugandan", "propagandist’s", "doppelganger’s", "manganese", "vegan", "hooligan’s",
                                "standard", "outstanding", "mandatory", "random", "bland", "handsome", "standalone", "grandiose", "handy", "incandescent", "outlandish", "demanding", "handmade", "handheld", "scandalous", "understandable", "Scandinavian", "broadband", "sandy", "upstanding", "Icelandic", "bandit’s", "candid", "contraband", "abandoned", "wandering", "expanded"]);
  animals = random_choice([[["crimson", "ruby", "vermilion", "rouge", "carmine", "bloody", "sanguine", "scarlet"], "wolf"],
                             [["island", "Hawaiian", "Tahitian",
                                 "tropical", "Samoan"], "rat"],
                             [["uninterested", "detached", "distant", "apathetic",
                                 "aloof", "nonchalant", "unresponsive"], "eel"],
                             [["normal", "average", "mundane", "mediocre",
                                 "standard", "ordinary"], "myna"],
                             [["maple", "yew", "oak", "willow",
                                 "pine", "balsa", "birch"], "grouse"],
                             [["dappled", "speckled", "dotted",
                                 "patchy", "sprinkled"], "hake"],
                             [["sovereign", "noble", "monarch", "emperor’s", "ruler’s", "patriarch"], "rail"]]);
  attribute2 = random_choice(animals[0]);
  attribute3 = random_choice(["ruthless", "religious", "rebellious", "repetitious", "reckless", "relentless", "rimless", "rigorous", "righteous", "ravenous", "ridiculous", "raucous", "rapacious",
                                "tallowy", "handsewn", "handdown", "sawn", "jackdaw’s", "markdown", "warhawk", "Malawi", "Jamestown",
                                "ubiquitous", "ominous", "frivolous", "uniform", "poisonous", "grievous", "oviparous", "ruinous", "blithesome", "rainproof", "odious",
                                "roundabout", "downbeat", "moonbeam", "thunderbolt", "paintball", "transcribing"]);
  base_item = random_choice(["armet", "cuirass", "eyeshield", "iron-mail", "linothorax", "neckguard", "overcoat", "scimitar", "tunic", "uniform", "bow", "dagger",
                               "falchion", "glaive", "halberd", "javelin", "katana", "mace", "pike", "quarterstaff", "rifle", "voulge", "whip", "xiphos", "yataghan", "zweihander"]);
  return attribute3 + " " + attribute1 + " " + attribute2 + " " + base_item + " of the " + animals[1] + " (level " + level + ")"
}


function getLootboxes(num) {
  if (num < 0) {
    return {'error' : 'Invalid number'};
  } else if (num > 10000) {
    return {'error' : "Slow down! Open at most 10000 lootboxes at a time."};
  } else {
    lootboxes = [];
    for (var i = 0; i < num; i++) {
      lootboxes[i] = generateLootbox();
    }
    return {'num': num, 'boxes': lootboxes};
  }
}

UNLOCKS = {
  'BATTLE': '../static/puzzle_resources/pride-and-accomplishment/images/battle.png',
  'CREATURE': '../static/puzzle_resources/pride-and-accomplishment/images/creature.png',
  'INOCULATE': '../static/puzzle_resources/pride-and-accomplishment/images/inoculate.png',
  'LIGAND': '../static/puzzle_resources/pride-and-accomplishment/images/ligand.png',
  'RAINBOWS': '../static/puzzle_resources/pride-and-accomplishment/images/rainbows.png'};

INDICES = {
    'BATTLE': 0,
    'CREATURE': 1,
    'INOCULATE': 2,
    'LIGAND': 3,
    'RAINBOWS': 4};

function unlockPremiumLootbox(requestData) {
  code = requestData['code'].toUpperCase().replace(/[^A-Z]/g, '');
  if (code in UNLOCKS) {
    return {
            'index': INDICES[code],
            'image': UNLOCKS[code]};
  } else {
    return {'error': 'Sorry, that unlock code is invalid.'}
  }
}

var main = function() {
    var doUnlock = function(data){
        $('#lootbox'+data.index).attr('src', data['image']);
    };

    var doOpen = function(data){
        $('#loot').html('');
        if(data['num'] == 1){
            $('#loot').append('<p>You opened a lootbox! It contained the following loot:</p>');
        }else{
            $('#loot').append('<p>You opened '+ data['num'] + ' lootboxes! They contained the following loot:</p>');
        }

        $('#loot').append('<ul id="lootList"></ul>');

        for(var i=0;i<data.num;i++){
            $('<li/>').text(data['boxes'][i]).appendTo('#lootList');
        }
    };

    $('#unlock').on('submit', function(){
        $('#unlock-error').html('');
        var requestData = {"code": $('#code').val().trim()};
        $('#code').val('');


        var responseData = unlockPremiumLootbox(requestData);
        if ("error" in responseData) {
          $('#unlock-error').html(responseData["error"]);
        } else {
          doUnlock(responseData);
        }

        return false;
    });

    $('#open').on('submit', function(){
        $('#open-error').html('');

        var responseData = getLootboxes(parseInt($('#num').val()));
        if ("error" in responseData) {
          $('#open-error').html(responseData["error"]);
        } else {
          doOpen(responseData);
        }
        return false;
    });
};

$(document).ready(main);
