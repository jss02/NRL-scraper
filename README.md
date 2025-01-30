# NRL-scraper
![NRL logo](/assets/nrllogos.jpg)
## Description
Web scraper for NRL.com matches written in Python.

## Features
- Scrapes data directly from NRL.com
- Filters out non-match related data such as images, metadata, etc.
- Scrapes all matches in a given round, year, or range of years
- Save as JSON files or into PostgreSQL database

## Installation
1. Clone repository:

```
git clone https://github.com/jss02/NRL-scraper.git
```

2. Navigate to project:

```
cd NRL-scraper
```

3. Install dependencies:

```
pip install -r requirements.txt
```

## Usage:
To get all matches from a round, run:

```
python3 src/round_scraper [year] [round] json
```

To get all matches from a year, run:

```
python3 src/year_scraper [year] json
```

To get all matches from a range of years, run:

```
python3 src/year_scraper [start year] [end year] json
```

To save results to a PostgreSQL database, use the above commands with
"json" replaced with 'psql'

> **NOTE**:
> PostgreSQL must be setup beforehand if saving to a psql database.

## Configuring psql
To save results to a PostgreSQL database, it must be setup and running beforehand. Afterwards, create a .env file in the root directory of the project in the format:

```
DB_NAME={db_name}
DB_USER={username}
DB_PASSWORD={password}
DB_HOST={host}
DB_PORT={port}
```

## License 
Creative Commons Attribution-NonCommercial 4.0 International License. View [License](https://creativecommons.org/licenses/by-nc/4.0/).