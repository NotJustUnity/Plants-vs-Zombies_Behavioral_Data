# Plants vs Zombies Behavioral Data

A web-based CSV editor application built with Flask for for previewing behavioral data of entities in PvZ.

![Preview](images\Preview.PNG)

## Overview

This application provides a web interface for viewing, editing, adding, and deleting rows in CSV files. It's designed for managing game entity configurations including sprites, types, and associated data.

## Features

- **Browse CSV files** - List and select from available CSV files
- **View CSV data** - Display file contents in an interactive table
- **Edit cells** - Update individual cell values
- **Add rows** - Append new rows to existing CSV files
- **Delete rows** - Remove rows from CSV files
- **Entity images** - Display entity images via CSV ImagePath references

## Project Structure

```
webapp/
├── app.py              # Flask application with API endpoints
├── README.md           # Project documentation (this file)
├── csv/                # Directory containing CSV data files
│   ├── entity.csv      # Entity configuration with image paths
│   ├── various CSV files for game data
│   └── specific/       # Entity-specific CSV files
├── static/             # Static assets (images, CSS)
│   ├── images/         # Entity sprite images
│   └── style.css       # Styling
└── templates/          # HTML templates
    └── index.html      # Main web interface
```

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/csv-list` | GET | List all CSV files in the csv/ directory |
| `/api/load-csv` | GET | Load and return CSV file contents |
| `/api/entity-image/<id>` | GET | Get image path for a given entity ID |
| `/edit-csv-cell` | POST | Edit a specific cell in a CSV file |
| `/delete-csv-row` | POST | Delete a row from a CSV file |
| `/add-csv-row` | POST | Add a new row to a CSV file |
| `/` | GET | Main web interface |

## Usage

1. Run venv .venv\Scripts\activate.bat
2. Run the application: `python app.py`
3. Open your browser to `http://127.0.0.1:5000`
4. Select a CSV file from the dropdown to view and edit its contents

## CSV Format

The `entity.csv` file uses this format:

```
EntityConfigId,ImagePath,Name,Type
sunflower,images/sunflower.jpg,Sunflower,Plant
peashooter,images/peashooter.webp,Peashooter,Plant
...
```

- `EntityConfigId` - Unique identifier for the entity
- `ImagePath` - Path to the entity's image (relative to static/)
- `Name` - Display name
- `Type` - Entity category/type

## Development

Built with Flask, using CSV files for data storage. Images are served from the `static/images/` directory.

## License

Proprietary - all rights reserved.