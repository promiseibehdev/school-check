# School Check

## Live Demo
https://school-check-vpkelphmqnu6aaek4qz3xp.streamlit.app/

## GitHub Repository
https://github.com/promiseibehdev/school-check

## Overview
School Check is a polished Streamlit application for discovering universities, tracking searches, and managing a shortlist of saved institutions. The project combines a lightweight SQLite database with live university data from the Universities API and a simple, professional dashboard experience.

## Features
- Search universities by name and country
- Prevent duplicate saves for the same institution
- Delete previously saved universities
- Review search history in a dedicated page
- Export saved universities to CSV
- View a weekly verification report simulation
- Maintain a simple, clean, and professional interface

## Tech Stack
- Python
- Streamlit
- SQLite
- Requests
- Pandas
- Pytest

## Installation
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```bash
   python init_db.py
   ```

## Usage
Run the application locally with:

```bash
streamlit run app.py
```

## Testing
Run the test suite with:

```bash
python -m pytest -q
```

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
├── data/
└── screenshots/
```

## Screenshots
Screenshots can be added to the [screenshots](screenshots/) folder. A placeholder guide is available in [screenshots/README.md](screenshots/README.md).

## License
MIT License

## Future Improvements
- Add richer university filters and comparison tools
- Expand the verification workflow with real data integrations
- Improve analytics and reporting for saved institutions
