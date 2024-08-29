from flask import Blueprint, request, jsonify

# Create a Blueprint
funcs_bp = Blueprint('funcs', __name__)

@funcs_bp.route('/calculate', methods=['POST'])
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
