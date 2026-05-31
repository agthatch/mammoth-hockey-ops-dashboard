# Mammoth Hockey Ops Dashboard

A hockey operations analytics dashboard focused on Utah Mammoth team performance.

This project is designed as an internal decision-support tool that transforms NHL game data into actionable insights for coaches, analysts, and hockey operations staff. The dashboard emphasizes performance trends, opponent analysis, and team-level analytics through interactive visualizations and data-driven reporting.

## Project Goals

### Version 1

Build a team analytics dashboard that provides:

* Team summary metrics
* Goals scored trends
* Goals allowed trends
* Goal differential trends
* Opponent analysis
* Recent game summaries

### Future Enhancements

Planned areas for expansion include:

* Player analytics
* Advanced hockey metrics
* Team comparisons
* Special teams analysis
* Additional data visualizations
* Cloud deployment
* CI/CD automation

## Tech Stack

### Backend

* Python 3.13
* FastAPI
* Pandas
* SQLite

### Frontend

* HTML5
* Vanilla JavaScript
* Tailwind CSS
* Highcharts

### Development Tools

* Git
* GitHub
* Cursor

## Data Sources

NHL API

Base URL:

```text
https://api-web.nhle.com/v1
```

Primary endpoints:

```text
/club-schedule-season/UTA/20262027
/gamecenter/{gameId}/boxscore
/gamecenter/{gameId}/play-by-play
```

## Architecture

```text
NHL API
    │
    ▼
FastAPI Services
    │
    ▼
SQLite Database
    │
    ▼
Pandas Analytics
    │
    ▼
REST API
    │
    ▼
HTML + JavaScript + Tailwind + Highcharts
```

## Planned Features

### Executive Summary

* Record
* Points
* Goals For
* Goals Against
* Goal Differential

### Performance Trends

* Goal differential trends
* Goals scored trends
* Goals allowed trends
* Rolling averages

### Opponent Analysis

* Opponent records
* Goal differential by opponent
* Performance comparisons

### Recent Games

* Game summaries
* Results
* Score trends

## Local Development

### Clone Repository

```bash
git clone https://github.com/<username>/mammoth-hockey-ops-dashboard.git
cd mammoth-hockey-ops-dashboard
```

### Backend Setup

```bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / Mac
source .venv/bin/activate

pip install -r requirements.txt
```

### Run Backend

```bash
uvicorn app.main:app --reload
```

Backend should be available at:

```text
http://localhost:8000
```

### Frontend

The frontend will be served locally during development and will consume data from the FastAPI backend.

## Development Philosophy

This project is intentionally built using modern AI-assisted development workflows while maintaining human ownership of:

* Architecture
* Requirements
* Design decisions
* Testing
* Code review

The goal is to demonstrate practical software engineering, analytics, and visualization skills using a modern development stack.

## License

MIT License
