from flask import Flask, jsonify, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__)

columns = ["num_1", "num_2", "num_3", "num_4", "num_5", "num_6", "num_7", "num_8", "num_9", "prize"]

# Define the rows as tuples with their respective repetitions
data = [
    (1, ["$20", "$20", "$10", "$1,000,000", "$1,000,000", "$1,000,000", "$10", "$10", "$100", "1000000"]),
    (3, ["$50", "$50", "$100", "$20,000", "$20,000", "$20,000", "$30", "$30", "$1,000", "20000"]),
    (3, ["$10,000", "$10,000", "$10,000", "$500", "$500", "$100", "$20", "$20", "$200", "10000"]),
    (5, ["$20,000", "$20,000", "$20", "$5,000", "$5,000", "$5,000", "$100", "$1,000", "$100", "5000"]),
    (430, ["$5,000", "$5,000", "$20", "$200", "$200", "$2,000", "$1,000", "$1,000", "$1,000", "1000"]),
    (967, ["$500", "$500", "$500", "$100", "$200", "$100", "$100", "$100", "$1,000", "500"]),
    (14875, ["$200", "$200", "$500", "$1,000", "$1,000", "$100", "$100", "$100", "$100", "100"]),
    (12223, ["$5,000", "$5,000", "$1,000", "$50", "$50", "$50", "$20", "$50", "$2,000", "50"]),
    (12227, ["$20", "$50", "$100", "$100", "$20", "$100", "$30", "$30", "$30", "30"]),
    (109905, ["$20", "$20", "$20", "$50", "$50", "$100", "$100", "$100", "$30", "20"]),
    (48833, ["$10,0000", "$10,0000", "$1,000", "$15", "$15", "$15", "$1,000", "$1,000", "$10", "15"]),
    (120951, ["$500", "$500", "$50", "$100", "$100", "$20", "$10", "$10", "$10", "10"]),
    (50951, ["$100", "$100", "$1,000", "$10", "$10", "$10", "$200", "$200", "$20", "10"]),
    (200000, ["$2,000", "$2,000", "$200", "$100", "$100", "$1,000", "$10,000", "$1,000", "$10,000", "0"]),
    (250657, ["$1,000,000", "$1,000,000", "$10,000", "$500", "$5,000", "$500", "$2,000", "$20,000", "$2,000", "0"]),
    (200000, ["$20,000", "$2,000", "$20,000", "$1000", "$100", "$10,000", "$10,000", "$1,000", "$10,000", "0"]),
    (200000, ["$5,000", "$500", "$500", "$100", "$100", "$1,000", "$10,000", "$1,000", "$10,000", "0"])
]

# Create the DataFrame by repeating rows
df = pd.DataFrame(
    np.repeat([entry[1] for entry in data], [entry[0] for entry in data], axis=0),
    columns=columns
)    
# Shuffle the DataFrame
df = df.sample(frac=1).reset_index(drop=True)

# Initialize variables
current_row = 0
total_prize = 0
tickets_scratched = 0

@app.route('/')
def index():
    global current_row
    # Send the current row values to the frontend
    row_values = df.iloc[current_row].to_dict()
    return render_template('index.html', row=row_values, total=total_prize, tickets_scratched=tickets_scratched)

@app.route('/reveal', methods=['POST'])
def reveal():
    global current_row, total_prize, tickets_scratched
    data = request.json
    # Get the value corresponding to the clicked box
    box_value = df.iloc[current_row][data['box']]
    
    # If all boxes are revealed, update the total prize and move to the next row
    if data['all_revealed']:
        total_prize += int(df.iloc[current_row]['prize'].replace(",", ""))-10
        current_row += 1
        tickets_scratched += 1
    
    return jsonify(value=box_value, total=total_prize)

@app.route('/reset', methods=['POST'])
def reset():
    global current_row
    # Get the next row's data after reset
    if current_row < len(df):
        row_values = df.iloc[current_row].to_dict()
        return jsonify(row=row_values, tickets_scratched=tickets_scratched)
    else:
        return jsonify(error="No more rows available")

if __name__ == '__main__':
    app.run(debug=True)