import os
import csv
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='templates', static_folder='static')

CSV_DIR = 'csv/'
ENTITY_FILE = 'entity.csv'


# --- API Routes ---

@app.route('/api/csv-list')
def api_csv_list():
    """Return list of CSV files including entity.csv"""
    try:
        all_files = [f for f in os.listdir(CSV_DIR) if f.endswith('.csv')]
        return jsonify(all_files)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route('/api/load-csv')
def api_load_csv():
    """Return contents of a CSV file"""
    filename = request.args.get('filename')
    if not filename:
        return jsonify(error='No filename provided'), 400

    csv_path = os.path.join(CSV_DIR, filename)
    if not os.path.exists(csv_path):
        return jsonify(error='File not found'), 404

    try:
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            data = [dict(row) for row in reader]

        return jsonify(
            filename=filename,
            headers=headers,
            data=data
        )
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route('/api/entity-image/<entity_id>')
def api_entity_image(entity_id):
    """Return image path for a given EntityConfigId"""
    try:
        entity_path = os.path.join(CSV_DIR, ENTITY_FILE)
        with open(entity_path, 'r') as e:
            reader = csv.DictReader(e)
            for row in reader:
                if row['EntityConfigId'] == entity_id:
                    return jsonify(imagePath=row.get('ImagePath', ''))
        return jsonify(imagePath=''), 404
    except Exception as ex:
        return jsonify(error=str(ex)), 500


# --- CSV Editing Endpoints ---

@app.route('/edit-csv-cell', methods=['POST'])
def edit_csv_cell():
    """Edit a specific cell in a CSV file"""
    try:
        data = request.json if request.is_json else request.form
        filename = data.get('filename')
        row_id = data.get('row_id')
        col_name = data.get('column')
        new_value = data.get('value')

        if not all([filename, row_id, col_name, new_value]):
            return jsonify(error='Missing required parameters'), 400

        csv_path = os.path.join(CSV_DIR, filename)
        if not os.path.exists(csv_path):
            return jsonify(error='File not found'), 404

        # Load CSV data
        with open(csv_path, 'r') as f:
            rows = list(csv.DictReader(f))

        # Use row_id as index
        try:
            row_idx = int(row_id)
            if row_idx < 0 or row_idx >= len(rows):
                return jsonify(error='Row index out of bounds'), 400
            if col_name not in rows[row_idx]:
                return jsonify(error='Column not found in row'), 400

            rows[row_idx][col_name] = new_value

            # Write back
            with open(csv_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

            return jsonify(success=True, updated_row_idx=row_idx, updated_column=col_name)
        except ValueError:
            return jsonify(error='Row ID must be an integer'), 400

    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route('/delete-csv-row', methods=['POST'])
def delete_csv_row():
    """Delete a row from a CSV file"""
    try:
        data = request.json if request.is_json else request.form
        filename = data.get('filename')
        row_id = data.get('row_id')

        if not filename:
            return jsonify(error='Filename is required'), 400

        csv_path = os.path.join(CSV_DIR, filename)
        if not os.path.exists(csv_path):
            return jsonify(error='File not found'), 404

        # Load CSV data
        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)

        if not rows:
            return jsonify(error='CSV file is empty'), 400

        headers = rows[0]
        data_rows = rows[1:]

        # Remove row by index
        try:
            row_idx = int(row_id)
            if row_idx < 0 or row_idx >= len(data_rows):
                return jsonify(error='Row index out of bounds'), 400
            data_rows.pop(row_idx)
        except ValueError:
            return jsonify(error='Row ID must be an integer'), 400

        # Write back
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(data_rows)

        return jsonify(success=True, deleted_row_idx=row_idx)

    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route('/add-csv-row', methods=['POST'])
def add_csv_row():
    """Add a new row to a CSV file"""
    try:
        data = request.json if request.is_json else request.form
        filename = data.get('filename')
        new_row_data = data.get('row_data', {})

        if not filename:
            return jsonify(error='Filename is required'), 400

        csv_path = os.path.join(CSV_DIR, filename)
        if not os.path.exists(csv_path):
            return jsonify(error='File not found'), 404

        # Load CSV data
        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)

        if not rows:
            return jsonify(error='CSV file is empty or has no headers'), 404

        # Extract headers from first row
        headers = rows[0]
        existing_rows = rows[1:]

        # Create new row with all headers (empty if not provided)
        new_row = []
        for header in headers:
            new_row.append(new_row_data.get(header, ''))

        # Append new row
        existing_rows.append(new_row)

        # Write back to file (headers + all data rows)
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(existing_rows)

        return jsonify(success=True, new_row_index=len(existing_rows) - 1)

    except Exception as e:
        return jsonify(error=str(e)), 500


# --- Main Page ---

@app.route('/')
def index():
    # We'll list CSV files via JS, but pass default set for SEO
    csv_files = [f for f in os.listdir(CSV_DIR) if f.endswith('.csv')]
    return render_template('index.html', csv_files=csv_files)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)