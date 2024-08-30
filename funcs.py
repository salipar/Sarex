from flask import Blueprint, request, jsonify
import networkx as nx
from itertools import combinations

# Create a Blueprint
funcs_bp = Blueprint('funcs', __name__)

def diffby1(word1, word2):
    if len(word1) != len(word2):
        return False

    differences = 0
    for char1, char2 in zip(word1, word2):
        if char1 != char2:
            differences += 1
        if differences > 1:
            return False

    return differences == 1


Words = (
    'able', \
    'acid', \
    'acre', \
    'aged', \
    'aide', \
    'akin', \
    'alas', \
    'ally', \
    'also', \
    'alto', \
    'amid', \
    'anal', \
    'anna', \
    'anti', \
    'apex', \
    'arch', \
    'area', \
    'army', \
    'atom', \
    'atop', \
    'aunt', \
    'aura', \
    'auto', \
    'avid', \
    'away', \
    'axis', \
    'baby', \
    'bach', \
    'back', \
    'bail', \
    'bait', \
    'bake', \
    'bald', \
    'ball', \
    'band', \
    'bang', \
    'bank', \
    'bare', \
    'bark', \
    'barn', \
    'base', \
    'bass', \
    'bath', \
    'bats', \
    'beam', \
    'bean', \
    'bear', \
    'beat', \
    'beck', \
    'beef', \
    'been', \
    'beer', \
    'bell', \
    'belt', \
    'bend', \
    'bent', \
    'best', \
    'beta', \
    'beth', \
    'bias', \
    'bike', \
    'bill', \
    'bind', \
    'bird', \
    'bite', \
    'blew', \
    'bloc', \
    'blog', \
    'blow', \
    'blue', \
    'blur', \
    'boat', \
    'body', \
    'boil', \
    'bold', \
    'bolt', \
    'bomb', \
    'bond', \
    'bone', \
    'book', \
    'boom', \
    'boon', \
    'boot', \
    'bore', \
    'born', \
    'boss', \
    'both', \
    'bout', \
    'bowl', \
    'brad', \
    'bred', \
    'brew', \
    'brow', \
    'buck', \
    'bulb', \
    'bulk', \
    'bull', \
    'bump', \
    'burn', \
    'bury', \
    'bush', \
    'bust', \
    'busy', \
    'butt', \
    'buzz', \
    'cafe', \
    'cage', \
    'cake', \
    'calf', \
    'call', \
    'calm', \
    'came', \
    'camp', \
    'cane', \
    'cape', \
    'card', \
    'care', \
    'carl', \
    'carr', \
    'cart', \
    'case', \
    'cash', \
    'cast', \
    'cave', \
    'cell', \
    'cent', \
    'chad', \
    'chap', \
    'chat', \
    'chef', \
    'chic', \
    'chin', \
    'chip', \
    'chop', \
    'cite', \
    'city', \
    'clad', \
    'clan', \
    'clay', \
    'clip', \
    'club', \
    'clue', \
    'coal', \
    'coat', \
    'coca', \
    'code', \
    'coil', \
    'coin', \
    'coke', \
    'cola', \
    'cold', \
    'cole', \
    'come', \
    'cone', \
    'conn', \
    'cook', \
    'cool', \
    'cope', \
    'copy', \
    'cord', \
    'core', \
    'cork', \
    'corn', \
    'cost', \
    'coup', \
    'cove', \
    'crap', \
    'crew', \
    'crop', \
    'crow', \
    'cube', \
    'cult', \
    'curb', \
    'cure', \
    'cute', \
    'dale', \
    'dame', \
    'damn', \
    'damp', \
    'dare', \
    'dark', \
    'dash', \
    'data', \
    'date', \
    'dawn', \
    'days', \
    'dead', \
    'deaf', \
    'deal', \
    'dean', \
    'dear', \
    'debt', \
    'deck', \
    'deed', \
    'deep', \
    'deer', \
    'dell', \
    'demo', \
    'dent', \
    'deny', \
    'desk', \
    'dial', \
    'dice', \
    'dick', \
    'diet', \
    'dire', \
    'dirt', \
    'disc', \
    'dish', \
    'disk', \
    'dive', \
    'dock', \
    'does', \
    'dole', \
    'doll', \
    'dome', \
    'done', \
    'doom', \
    'door', \
    'dose', \
    'dove', \
    'down', \
    'drag', \
    'draw', \
    'drew', \
    'drop', \
    'drug', \
    'drum', \
    'dual', \
    'duck', \
    'duff', \
    'duke', \
    'dull', \
    'duly', \
    'dumb', \
    'dump', \
    'dusk', \
    'dust', \
    'duty', \
    'each', \
    'earl', \
    'earn', \
    'ease', \
    'east', \
    'easy', \
    'eats', \
    'echo', \
    'edge', \
    'edit', \
    'else', \
    'envy', \
    'epic', \
    'euro', \
    'even', \
    'ever', \
    'evil', \
    'exam', \
    'exit', \
    'expo', \
    'eyed', \
    'face', \
    'fact', \
    'fade', \
    'fail', \
    'fair', \
    'fake', \
    'fall', \
    'fame', \
    'fare', \
    'farm', \
    'fast', \
    'fate', \
    'fear', \
    'feat', \
    'feed', \
    'feel', \
    'feet', \
    'fell', \
    'felt', \
    'file', \
    'fill', \
    'film', \
    'find', \
    'fine', \
    'fire', \
    'firm', \
    'fish', \
    'fist', \
    'five', \
    'flag', \
    'flat', \
    'fled', \
    'flee', \
    'flew', \
    'flex', \
    'flip', \
    'flow', \
    'flux', \
    'foam', \
    'foil', \
    'fold', \
    'folk', \
    'fond', \
    'font', \
    'food', \
    'fool', \
    'foot', \
    'ford', \
    'fore', \
    'fork', \
    'form', \
    'fort', \
    'foul', \
    'four', \
    'free', \
    'frog', \
    'from', \
    'fuck', \
    'fuel', \
    'full', \
    'fund', \
    'fury', \
    'fuse', \
    'fuss', \
    'gain', \
    'gala', \
    'gale', \
    'gall', \
    'game', \
    'gang', \
    'gate', \
    'gave', \
    'gaze', \
    'gear', \
    'gene', \
    'gift', \
    'gill', \
    'girl', \
    'give', \
    'glad', \
    'glen', \
    'glow', \
    'glue', \
    'goal', \
    'goat', \
    'goes', \
    'gold', \
    'golf', \
    'gone', \
    'good', \
    'gore', \
    'gown', \
    'grab', \
    'gram', \
    'gray', \
    'grew', \
    'grey', \
    'grid', \
    'grim', \
    'grin', \
    'grip', \
    'grow', \
    'gulf', \
    'guru', \
    'hail', \
    'hair', \
    'hale', \
    'half', \
    'hall', \
    'halt', \
    'hand', \
    'hang', \
    'hank', \
    'hard', \
    'harm', \
    'hart', \
    'hate', \
    'haul', \
    'have', \
    'hawk', \
    'head', \
    'heal', \
    'heap', \
    'hear', \
    'heat', \
    'heel', \
    'heir', \
    'held', \
    'hell', \
    'helm', \
    'help', \
    'herb', \
    'herd', \
    'here', \
    'hero', \
    'hers', \
    'hide', \
    'high', \
    'hike', \
    'hill', \
    'hint', \
    'hire', \
    'hold', \
    'hole', \
    'holt', \
    'holy', \
    'home', \
    'hood', \
    'hook', \
    'hope', \
    'horn', \
    'hose', \
    'host', \
    'hour', \
    'huge', \
    'hull', \
    'hung', \
    'hunt', \
    'hurt', \
    'hype', \
    'icon', \
    'idea', \
    'idle', \
    'idol', \
    'inch', \
    'info', \
    'into', \
    'iris', \
    'iron', \
    'isle', \
    'item', \
    'jack', \
    'jail', \
    'jake', \
    'jane', \
    'java', \
    'jazz', \
    'jean', \
    'jeep', \
    'jill', \
    'joey', \
    'john', \
    'join', \
    'joke', \
    'josh', \
    'jump', \
    'junk', \
    'jury', \
    'just', \
    'keen', \
    'keep', \
    'kemp', \
    'kent', \
    'kept', \
    'khan', \
    'kick', \
    'kill', \
    'kind', \
    'king', \
    'kirk', \
    'kiss', \
    'kite', \
    'knee', \
    'knew', \
    'knit', \
    'knot', \
    'know', \
    'kohl', \
    'Kyle', \
    'lace', \
    'lack', \
    'lady', \
    'laid', \
    'lake', \
    'lamb', \
    'lamp', \
    'land', \
    'lane', \
    'lang', \
    'last', \
    'late', \
    'lava', \
    'lawn', \
    'lazy', \
    'lead', \
    'leaf', \
    'leak', \
    'lean', \
    'leap', \
    'left', \
    'lend', \
    'lens', \
    'lent', \
    'less', \
    'lest', \
    'levy', \
    'lied', \
    'lien', \
    'life', \
    'lift', \
    'like', \
    'lily', \
    'limb', \
    'lime', \
    'limp', \
    'line', \
    'link', \
    'lion', \
    'list', \
    'live', \
    'load', \
    'loan', \
    'lock', \
    'loft', \
    'logo', \
    'lone', \
    'long', \
    'look', \
    'loop', \
    'lord', \
    'lose', \
    'loss', \
    'lost', \
    'loud', \
    'love', \
    'luck', \
    'lump', \
    'lung', \
    'lure', \
    'lush', \
    'lust', \
    'made', \
    'maid', \
    'mail', \
    'main', \
    'make', \
    'male', \
    'mall', \
    'mama', \
    'many', \
    'marc', \
    'mark', \
    'mart', \
    'mask', \
    'mass', \
    'mate', \
    'matt', \
    'mayo', \
    'maze', \
    'mead', \
    'meal', \
    'mean', \
    'meat', \
    'meet', \
    'Mega', \
    'melt', \
    'memo', \
    'menu', \
    'mere', \
    'mesa', \
    'mesh', \
    'mess', \
    'mice', \
    'mick', \
    'mike', \
    'mild', \
    'mile', \
    'milk', \
    'mill', \
    'mind', \
    'mine', \
    'mini', \
    'mint', \
    'miss', \
    'mist', \
    'mock', \
    'mode', \
    'mold', \
    'monk', \
    'mood', \
    'moon', \
    'more', \
    'moss', \
    'most', \
    'move', \
    'much', \
    'must', \
    'myth', \
    'nail', \
    'name', \
    'navy', \
    'near', \
    'neat', \
    'neck', \
    'need', \
    'nest', \
    'news', \
    'next', \
    'nice', \
    'nick', \
    'nine', \
    'node', \
    'none', \
    'noon', \
    'norm', \
    'nose', \
    'note', \
    'nova', \
    'nude', \
    'nuts', \
    'oath', \
    'obey', \
    'odds', \
    'odor', \
    'okay', \
    'once', \
    'only', \
    'onto', \
    'open', \
    'oral', \
    'otto', \
    'ours', \
    'oval', \
    'oven', \
    'over', \
    'pace', \
    'pack', \
    'pact', \
    'page', \
    'paid', \
    'pain', \
    'pair', \
    'pale', \
    'palm', \
    'papa', \
    'para', \
    'park', \
    'part', \
    'pass', \
    'past', \
    'path', \
    'peak', \
    'peat', \
    'peck', \
    'peel', \
    'peer', \
    'pest', \
    'pick', \
    'pier', \
    'pike', \
    'pile', \
    'pill', \
    'pine', \
    'pink', \
    'pint', \
    'pipe', \
    'pity', \
    'plan', \
    'play', \
    'plea', \
    'plot', \
    'plug', \
    'plus', \
    'poem', \
    'poet', \
    'pole', \
    'poll', \
    'polo', \
    'poly', \
    'pond', \
    'pony', \
    'pool', \
    'poor', \
    'pope', \
    'pork', \
    'port', \
    'pose', \
    'post', \
    'pour', \
    'pray', \
    'prep', \
    'prey', \
    'prof', \
    'prop', \
    'pull', \
    'pulp', \
    'pump', \
    'punk', \
    'pure', \
    'push', \
    'quid', \
    'quit', \
    'quiz', \
    'race', \
    'rack', \
    'rage', \
    'raid', \
    'rail', \
    'rain', \
    'ramp', \
    'rang', \
    'rank', \
    'rape', \
    'rare', \
    'rash', \
    'rate', \
    'rave', \
    'read', \
    'real', \
    'reap', \
    'rear', \
    'reed', \
    'reef', \
    'reel', \
    'rely', \
    'rent', \
    'rest', \
    'rice', \
    'rich', \
    'rick', \
    'ride', \
    'ring', \
    'riot', \
    'ripe', \
    'rise', \
    'risk', \
    'rite', \
    'ritz', \
    'road', \
    'roar', \
    'rock', \
    'rode', \
    'role', \
    'roll', \
    'roof', \
    'room', \
    'root', \
    'rope', \
    'rose', \
    'ruby', \
    'rude', \
    'ruin', \
    'rule', \
    'rush', \
    'rust', \
    'ruth', \
    'sack', \
    'safe', \
    'saga', \
    'sage', \
    'said', \
    'sail', \
    'sake', \
    'sale', \
    'salt', \
    'same', \
    'sand', \
    'sang', \
    'sank', \
    'save', \
    'scan', \
    'scar', \
    'scot', \
    'seal', \
    'seat', \
    'seed', \
    'seek', \
    'seem', \
    'seen', \
    'self', \
    'sell', \
    'semi', \
    'send', \
    'sent', \
    'sept', \
    'sexy', \
    'shah', \
    'shed', \
    'ship', \
    'shit', \
    'shoe', \
    'shop', \
    'shot', \
    'show', \
    'shut', \
    'sick', \
    'side', \
    'sigh', \
    'sign', \
    'silk', \
    'sing', \
    'sink', \
    'site', \
    'size', \
    'skin', \
    'skip', \
    'slab', \
    'slam', \
    'slap', \
    'slid', \
    'slim', \
    'slip', \
    'slot', \
    'slow', \
    'snap', \
    'snow', \
    'soap', \
    'soar', \
    'soda', \
    'sofa', \
    'soft', \
    'soil', \
    'sold', \
    'sole', \
    'solo', \
    'some', \
    'song', \
    'soon', \
    'sore', \
    'sort', \
    'soul', \
    'soup', \
    'sour', \
    'span', \
    'spin', \
    'spit', \
    'spot', \
    'spun', \
    'spur', \
    'star', \
    'stay', \
    'stem', \
    'step', \
    'stir', \
    'stop', \
    'such', \
    'suck', \
    'suit', \
    'sung', \
    'sunk', \
    'sure', \
    'surf', \
    'swan', \
    'swap', \
    'sway', \
    'swim', \
    'tack', \
    'tail', \
    'take', \
    'tale', \
    'talk', \
    'tall', \
    'tank', \
    'tape', \
    'taps', \
    'task', \
    'taxi', \
    'team', \
    'tear', \
    'tech', \
    'teen', \
    'tell', \
    'tend', \
    'tent', \
    'term', \
    'test', \
    'text', \
    'than', \
    'that', \
    'them', \
    'then', \
    'they', \
    'thin', \
    'this', \
    'thou', \
    'thus', \
    'tick', \
    'tide', \
    'tidy', \
    'tier', \
    'tile', \
    'till', \
    'tilt', \
    'time', \
    'tiny', \
    'tire', \
    'toby', \
    'told', \
    'toll', \
    'tomb', \
    'tone', \
    'tony', \
    'took', \
    'tool', \
    'tops', \
    'tore', \
    'torn', \
    'tort', \
    'toss', \
    'tour', \
    'town', \
    'trap', \
    'tray', \
    'tree', \
    'trek', \
    'trim', \
    'trio', \
    'trip', \
    'troy', \
    'TRUE', \
    'tube', \
    'tuck', \
    'tuna', \
    'tune', \
    'turf', \
    'turn', \
    'twin', \
    'type', \
    'ugly', \
    'unit', \
    'upon', \
    'urge', \
    'used', \
    'user', \
    'vain', \
    'vary', \
    'vast', \
    'veil', \
    'vein', \
    'verb', \
    'very', \
    'vest', \
    'veto', \
    'vice', \
    'view', \
    'vine', \
    'visa', \
    'void', \
    'vote', \
    'wade', \
    'wage', \
    'wait', \
    'wake', \
    'walk', \
    'wall', \
    'want', \
    'ward', \
    'ware', \
    'warm', \
    'warn', \
    'wary', \
    'wash', \
    'watt', \
    'wave', \
    'ways', \
    'weak', \
    'wear', \
    'weed', \
    'week', \
    'well', \
    'went', \
    'were', \
    'west', \
    'what', \
    'when', \
    'whip', \
    'whom', \
    'wide', \
    'wife', \
    'wild', \
    'will', \
    'wind', \
    'wine', \
    'wing', \
    'wipe', \
    'wire', \
    'wise', \
    'wish', \
    'with', \
    'woke', \
    'wolf', \
    'wood', \
    'wool', \
    'word', \
    'wore', \
    'work', \
    'worm', \
    'worn', \
    'wrap', \
    'yang', \
    'yard', \
    'yarn', \
    'yeah', \
    'year', \
    'your', \
    'yuan', \
    'zero', \
    'zinc', \
    'zone', \
    'plod', \
    'quad', \
    'bass', \
    'ally', \
    'plop', \
    'zoom'

)

mG = nx.Graph()
mG.add_nodes_from(Words)

print('Adding edges')
for apair in combinations(Words, 2):
    w1, w2 = apair
    if diffby1(w1, w2):
        mG.add_edge(w1, w2)

print('Completed adding edges')


@funcs_bp.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        # Retrieve input values from the form
        num1 = float(request.form.get('num1'))
        num2 = float(request.form.get('num2'))

        # Perform the calculation (e.g., sum)
        result = num1 + num2  # Replace this with your desired calculation

        # Return the result as JSON
        return jsonify({'result': result})
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid input. Please enter valid numbers.'})

@funcs_bp.route('/api/wordpath', methods=['POST'])
def wordpath():
    ErrorMsg, L = '', []
    sourceword = request.form['sourceword']
    targetword = request.form['targetword']
    try:
        L = nx.shortest_path(mG, sourceword, targetword)
    except nx.NetworkXNoPath:
        ErrorMsg = 'In the current dictionary, there is no way to reach from ' + sourceword + ' to ' + targetword + '.'
    except nx.NodeNotFound:
        ErrorMsg = 'Either ' + sourceword + ' or ' + targetword + ' is not in the dictionary.'
    #print('nodes', nx.number_of_nodes(mG), nx.shortest_path(sourceword, targetword))
    return jsonify({'result': L, 'error': ErrorMsg})
