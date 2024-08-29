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


Words = ('about',	'above',	'abuse',	'actor',	'acute',	'admit',	'adopt',	'adult',	'after',	'again',	'agent',	'agree',	'ahead',	'alarm',	'album',	'boost',	'booth',	'bound',	'brain',	'brand',	'bread',	'break',	'breed',	'brief',	'bring',	'broad',	'broke',	'brown',	'build',	'built',	'debut',	'delay',	'depth',	'doing',	'doubt',	'dozen',	'draft',	'drama',	'drawn',	'dream',	'dress',	'drill',	'drink',	'drive',	'drove',	'dying',	'eager',	'early',	'earth',	'eight',	'elite',	'empty',	'enemy',	'enjoy',	'enter',	'judge',	'known',	'label',	'large',	'laser',	'later',	'laugh',	'layer',	'learn',	'lease',	'least',	'leave',	'legal',	'level',	'light',	'limit',	'peace',	'panel',	'phase',	'phone',	'photo',	'piece',	'pilot',	'pitch',	'place',	'plain',	'plane',	'plant',	'plate',	'point',	'pound',	'sheet',	'shelf',	'shell',	'shift',	'shirt',	'shock',	'shoot',	'short',	'shown',	'sight',	'since',	'sixty',	'sized',	'skill',	'sleep',	'slide',	'small',	'smart',	'smile',	'smith',	'smoke',	'solid',	'solve',	'sorry',	'sound',	'south',	'space',	'upset',	'urban',	'usage',	'usual',	'valid',	'value',	'video',	'virus',	'visit',	'beach',	'began',	'begin',	'begun',	'being',	'below',	'bench',	'billy',	'birth',	'black',	'blame',	'blind',	'block',	'blood',	'board',	'cover',	'craft',	'crash',	'cream',	'crime',	'cross',	'crowd',	'crown',	'curve',	'cycle',	'daily',	'dance',	'dated',	'dealt',	'death',	'group',	'grown',	'guard',	'guess',	'guest',	'guide',	'happy',	'harry',	'heart',	'heavy',	'hence',	'night',	'horse',	'hotel',	'house',	'human',	'ideal',	'image',	'index',	'inner',	'input',	'issue',	'irony',	'juice',	'joint',	'newly',	'noise',	'north',	'noted',	'novel',	'nurse',	'occur',	'ocean',	'offer',	'often',	'order',	'other',	'ought',	'paint',	'paper',	'party',	'round',	'route',	'royal',	'rural',	'scale',	'scene',	'scope',	'score',	'sense',	'serve',	'seven',	'shall',	'shape',	'share',	'sharp',	'times',	'tired',	'title',	'today',	'topic',	'total',	'touch',	'tough',	'tower',	'track',	'trade',	'treat',	'trend',	'trial',	'tried',	'tries',	'truck',	'truly',	'trust',	'truth',	'twice',	'under',	'undue',	'union',	'unity',	'until',	'upper',	'wound',	'write',	'wrong',	'wrote',	'yield',	'young',	'youth',	'worth',	'voice',	'argue',	'arise',	'array',	'aside',	'asset',	'audio',	'audit',	'avoid',	'award',	'aware',	'badly',	'baker',	'bases',	'basic',	'basis',	'china',	'chose',	'civil',	'claim',	'class',	'clean',	'clear',	'click',	'clock',	'close',	'coach',	'coast',	'could',	'count',	'court',	'forth',	'forty',	'forum',	'found',	'frame',	'frank',	'fraud',	'fresh',	'front',	'fruit',	'fully',	'funny',	'giant',	'given',	'glass',	'globe',	'going',	'grace',	'grade',	'grand',	'grant',	'grass',	'great',	'green',	'gross',	'media',	'might',	'minor',	'minus',	'mixed',	'model',	'money',	'month',	'moral',	'motor',	'mount',	'mouse',	'mouth',	'movie',	'needs',	'never',	'radio',	'raise',	'range',	'rapid',	'ratio',	'reach',	'ready',	'refer',	'right',	'rival',	'river',	'quick',	'stand',	'roman',	'rough',	'style',	'sugar',	'suite',	'super',	'sweet',	'table',	'taken',	'taste',	'taxes',	'teach',	'teeth',	'texas',	'thank',	'theft',	'their',	'theme',	'there',	'these',	'thick',	'thing',	'think',	'third',	'those',	'three',	'threw',	'throw',	'tight',	'waste',	'watch',	'water',	'wheel',	'where',	'which',	'while',	'white',	'vital',	'alert',	'alike',	'alive',	'allow',	'alone',	'along',	'alter',	'among',	'anger',	'angle',	'angry',	'apart',	'apple',	'apply',	'arena',	'buyer',	'cable',	'calif',	'carry',	'catch',	'cause',	'chain',	'chair',	'chart',	'chase',	'cheap',	'check',	'chest',	'chief',	'child',	'entry',	'equal',	'error',	'event',	'every',	'exact',	'exist',	'extra',	'faith',	'false',	'fault',	'fibre',	'field',	'fifth',	'fifty',	'fight',	'final',	'first',	'fixed',	'flash',	'fleet',	'floor',	'fluid',	'focus',	'force',	'metal',	'local',	'logic',	'loose',	'lower',	'lucky',	'lunch',	'lying',	'magic',	'major',	'maker',	'march',	'music',	'match',	'mayor',	'meant',	'power',	'press',	'price',	'pride',	'prime',	'print',	'prior',	'prize',	'proof',	'proud',	'prove',	'queen',	'sixth',	'quiet',	'quite',	'spare',	'speak',	'speed',	'spend',	'spent',	'split',	'spoke',	'sport',	'staff',	'stage',	'stake',	'start',	'state',	'steam',	'steel',	'stick',	'still',	'stock',	'stone',	'stood',	'store',	'storm',	'story',	'strip',	'stuck',	'study',	'stuff',	'whole',	'whose',	'woman',	'train',	'world',	'worry',	'worse',	'worst',	'would'	
)

mG = nx.Graph()
mG.add_nodes_from(Words)

for apair in combinations(Words, 2):
    w1, w2 = apair
    if diffby1(w1, w2):
        mG.add_edge(w1, w2)



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
    
    sourceword = request.form['sourceword']
    targetword = request.form['targetword']

    L = nx.shortest_path(mG, sourceword, targetword)
    #print('nodes', nx.number_of_nodes(mG), nx.shortest_path(sourceword, targetword))
    return jsonify({'result': L})
