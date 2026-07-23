# School Check

School Check is a polished Streamlit application for discovering universities, tracking searches, and managing a shortlist of saved institutions. The project combines a lightweight SQLite database with live university search data from the Universities API and a simple, professional dashboard experience.

## Features

- Search universities by name and country
- Prevent duplicate saves for the same institution
- Delete previously saved universities
- Review search history in a dedicated page
- Export saved universities to CSV
- Review a weekly verification report simulation
- Keep the interface simple, clean, and professional

## Tech Stack

- Python
- Streamlit
- SQLite
- Requests
- Pandas
- Pytest

## Project Structure

```text
school-check/
├── app.py
├── init_db.py
├── requirements.txt
├── src/
│   ├── database/
│   ├── services/
│   └── main.py
├── tests/
└── data/
```

## Getting Started

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```bash
   python init_db.py
   ```
4. Launch the app:
   ```bash
   streamlit run app.py
   ```

## Testing

Run the test suite with:

```bash
python -m pytest -q
```

## License

MIT License
