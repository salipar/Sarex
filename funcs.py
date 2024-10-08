from flask import Blueprint, request, jsonify, render_template, redirect, url_for
import networkx as nx
from itertools import combinations
import sqlite3

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

Words = []
mG = nx.Graph()

def BuildGraph():
    global Words, mG
    # Connect to the SQLite database
    conn = sqlite3.connect('words.db')
    
    # Create a cursor object
    cursor = conn.cursor()
    
    # SQL command to select all words from the Word table
    select_query = '''
    SELECT Word FROM Word order by Word
    '''
    
    # Execute the SQL command and fetch all results
    cursor.execute(select_query)
    words = cursor.fetchall()
    
    # Populate a list with just the words
    Words = [word[0].lower() for word in words]
    
    # Close the connection
    conn.close()
    
    mG.add_nodes_from(Words)

    print('Adding edges')
    for apair in combinations(Words, 2):
        w1, w2 = apair
        if diffby1(w1, w2):
            mG.add_edge(w1, w2)
    
    print('Completed adding edges')

BuildGraph()

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
    global Words, mG
    
    ErrorMsg, L = '', []
    sourceword = request.form['sourceword']
    targetword = request.form['targetword']

    if sourceword not in Words and targetword not in Words:
        ErrorMsg = 'Both ' + sourceword + ' and ' + targetword + ' are not in the dictionay.'
        L = [sourceword, targetword]
    elif sourceword not in Words:
        ErrorMsg = sourceword + ' is not in the dictionay.'
        L = [sourceword]
    elif targetword not in Words:
        ErrorMsg = targetword + ' is not in the dictionay.'
        L = [targetword]
        
    else:       
        try:
            L = list(nx.all_shortest_paths(mG, sourceword, targetword))
        except nx.NetworkXNoPath:
            ErrorMsg = 'In the current dictionary, there is no way to reach from ' + sourceword + ' to ' + targetword + '.'

    return jsonify({'result': L, 'error': ErrorMsg})


@funcs_bp.route('/api/addwords', methods=['POST'])
def add_words():
    data = request.json
    words = data.get('words', [])

    try:
        conn = sqlite3.connect('words.db')
        cursor = conn.cursor()

        # Assuming there's a table named 'word' with a column 'word'
        cursor.executemany('INSERT OR IGNORE INTO Word (word) VALUES (?)', [(word,) for word in words])

        conn.commit()
        conn.close()
        
        BuildGraph()
        
        return jsonify({'success': True})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'error': str(e)})


@funcs_bp.route('/vwords')
def view_words():
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()

    cur = cursor.execute('SELECT Word FROM Word WHERE source IS NULL ORDER BY Word')
    words = cur.fetchall()
    conn.close()

    return render_template('newwords.html', words=words)

@funcs_bp.route('/managenewwords', methods=['POST'])
def managenewwords():
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()

    actions = []
    for i in range(1, len(request.form)//2 + 1):
        word = request.form.get(f'word_{i}')
        action = request.form.get(f'action_{i}')

        if action == 'delete':
            cursor.execute('DELETE FROM Word WHERE Word = ?', (word,))
        elif action == 'save':
            cursor.execute('UPDATE Word SET source = ? WHERE Word = ?', ('W', word))
        # Ignore Now means do nothing, so no SQL operation for that case

    conn.commit()
    conn.close()

    return redirect(url_for('funcs.view_words'))

   


