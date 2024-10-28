from flask import Flask, jsonify, request, render_template, redirect, url_for
import threading


# Initialize Flask app
app = Flask(__name__)

class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.type = node_type  # "operator" or "operand"
        self.value = value  # e.g., age > 30
        self.left = left  # Left child (for operators)
        self.right = right  # Right child (for operators)

    def __repr__(self):
        return f"Node({self.type}, {self.value})"

# Sample In-memory Storage for Rules
rule_store = {}

# Pre-defined data for evaluation
data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}

# Function to create a rule (Converts rule string to AST)
def create_rule(rule_string):
    if "AND" in rule_string:
        parts = rule_string.split("AND")
        left = parts[0].strip()
        right = parts[1].strip()
        root = Node("operator", "AND")
        root.left = Node("operand", left)
        root.right = Node("operand", right)
    elif "OR" in rule_string:
        parts = rule_string.split("OR")
        left = parts[0].strip()
        right = parts[1].strip()
        root = Node("operator", "OR")
        root.left = Node("operand", left)
        root.right = Node("operand", right)
    else:
        root = Node("operand", rule_string.strip())

    return root

# Function to combine multiple rules
def combine_rules(rules, operator="AND"):
    combined_root = Node("operator", operator)
    current = combined_root

    for i, rule in enumerate(rules):
        if i == 0:
            current.left = rule_store[rule]
        else:
            current.right = rule_store[rule]
            if i < len(rules) - 1:
                new_node = Node("operator", operator)
                current.right = new_node
                current = new_node

    return combined_root

# Enhanced function to evaluate a rule against the data set
def evaluate_rule(ast, data):
    if ast.type == "operand":
        condition = ast.value.strip()

        # Handling different comparison operators
        if ">=" in condition:
            attribute, value = condition.split(">=")
            attribute = attribute.strip()
            value = int(value.strip())
            return data.get(attribute) >= value
        
        elif "<=" in condition:
            attribute, value = condition.split("<=")
            attribute = attribute.strip()
            value = int(value.strip())
            return data.get(attribute) <= value
        
        elif ">" in condition:
            attribute, value = condition.split(">")
            attribute = attribute.strip()
            value = int(value.strip())
            return data.get(attribute) > value
        
        elif "<" in condition:
            attribute, value = condition.split("<")
            attribute = attribute.strip()
            value = int(value.strip())
            return data.get(attribute) < value
        
        elif "==" in condition:
            attribute, value = condition.split("==")
            attribute = attribute.strip()
            value = value.strip().replace('"', '')  # For string comparisons
            return data.get(attribute) == value
        
    elif ast.type == "operator":
        left_eval = evaluate_rule(ast.left, data)
        right_eval = evaluate_rule(ast.right, data)

        if ast.value == "AND":
            return left_eval and right_eval
        elif ast.value == "OR":
            return left_eval or right_eval
        
    return False

# API endpoint to create a rule
@app.route('/api/create_rule', methods=['POST'])
def api_create_rule():
    rule_name = request.json.get('name')
    rule_string = request.json.get('rule')

    if rule_name and rule_string:
        rule_store[rule_name] = create_rule(rule_string)
        return jsonify({"message": f"Rule '{rule_name}' created!"}), 201
    return jsonify({"error": "Invalid input"}), 400

# API endpoint to combine rules
@app.route('/api/combine_rules', methods=['POST'])
def api_combine_rules():
    rule_name = request.json.get('name')
    rule_list = request.json.get('rules')
    operator = request.json.get('operator')

    if rule_name and rule_list and operator in ["AND", "OR"]:
        combined_ast = combine_rules(rule_list, operator)
        rule_store[rule_name] = combined_ast
        return jsonify({"message": f"Combined rule '{rule_name}' created!"}), 201
    return jsonify({"error": "Invalid input"}), 400

# API endpoint to evaluate a rule
@app.route("/api/evaluate_rule", methods=['POST'])
def api_evaluate_rule():
    rule_name = request.json.get('name')

    if rule_name in rule_store:
        result = evaluate_rule(rule_store[rule_name], data)
        return jsonify({"result": result}), 200
    return jsonify({"error": f"Rule '{rule_name}' does not exist."}), 404

#fetching the current rules

@app.route('/api/get_rules', methods=['GET'])
def get_rules():
    return jsonify({name: rule.value for name, rule in rule_store.items()}), 200

# Route for the web application
@app.route('/')
def index():
    return render_template('index.html', rules=rule_store)



# Function to run Flask app in a separate thread
def run_flask():
    app.run(port=5000)

if __name__ == "__main__":
    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
