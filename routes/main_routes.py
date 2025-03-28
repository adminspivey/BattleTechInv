from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for miniatures (can be replaced by a database later)
miniatures = []

@app.route('/')
def index():
    # Get filtering parameters from the URL query
    era_filter = request.args.getlist('era')
    unit_type_filter = request.args.getlist('unit_type')
    weight_class_filter = request.args.getlist('weight_class')
    weapons_filter = request.args.getlist('weapons')
    equipment_filter = request.args.getlist('equipment')
    
    filtered_miniatures = miniatures
    
    # Filter the miniatures based on selected filters
    if era_filter:
        filtered_miniatures = [m for m in filtered_miniatures if any(e in m['era'] for e in era_filter)]
    if unit_type_filter:
        filtered_miniatures = [m for m in filtered_miniatures if m['unit_type'] in unit_type_filter]
    if weight_class_filter:
        filtered_miniatures = [m for m in filtered_miniatures if m['weight_class'] in weight_class_filter]
    if weapons_filter:
        filtered_miniatures = [m for m in filtered_miniatures if any(w in m['weapons'] for w in weapons_filter)]
    if equipment_filter:
        filtered_miniatures = [m for m in filtered_miniatures if any(eq in m['equipment'] for eq in equipment_filter)]
    
    # Sort miniatures alphabetically by name
    filtered_miniatures.sort(key=lambda x: x['name'].lower())
    
    return render_template('index.html', miniatures=filtered_miniatures)

@app.route('/add_miniature', methods=['POST'])
def add_miniature():
    name = request.form['name'].strip()
    era = request.form.getlist('era')
    unit_type = request.form['unit_type']
    weight_class = request.form['weight_class']
    weapons = request.form.getlist('weapons')
    equipment = request.form.getlist('equipment')
    quantity = int(request.form['quantity'])
    
    # Check if the miniature already exists (by comparing all fields)
    for mini in miniatures:
        if (mini['name'].lower() == name.lower() and mini['era'] == era and mini['unit_type'] == unit_type and
            mini['weight_class'] == weight_class and mini['weapons'] == weapons and mini['equipment'] == equipment):
            mini['quantity'] += quantity  # If it exists, just increase the quantity
            return redirect(url_for('index'))
    
    # If not found, add the new miniature to the list
    miniatures.append({
        'name': name,
        'era': era,
        'unit_type': unit_type,
        'weight_class': weight_class,
        'weapons': weapons,
        'equipment': equipment,
        'quantity': quantity
    })
    
    return redirect(url_for('index'))

@app.route('/delete_miniature', methods=['POST'])
def delete_miniature():
    name = request.form['name'].strip()
    era = request.form.getlist('era')
    unit_type = request.form['unit_type']
    weight_class = request.form['weight_class']
    weapons = request.form.getlist('weapons')
    equipment = request.form.getlist('equipment')
    
    # Find the miniature and remove or reduce quantity
    for mini in miniatures:
        if (mini['name'].lower() == name.lower() and mini['era'] == era and mini['unit_type'] == unit_type and
            mini['weight_class'] == weight_class and mini['weapons'] == weapons and mini['equipment'] == equipment):
            if mini['quantity'] > 1:
                mini['quantity'] -= 1  # Decrease the quantity if more than 1
            else:
                miniatures.remove(mini)  # Remove the miniature if the quantity is 1
            break
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
