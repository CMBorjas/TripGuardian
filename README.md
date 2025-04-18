# TripGuardian: Predictive Maintenance Risk Scoring for RTD Bus Stops

**TripGuardian** is a data-driven AI tool that predicts which RTD (Regional Transportation District) bus stops are at higher risk of maintenance needs. It combines public safety data, transit schedules, and spatial analysis to support better infrastructure planning and rider experience.

---

## Problem Statement

Public transportation stops in high-crime or high-traffic areas are more likely to experience delays, detours, and maintenance issues. However, transit systems rarely prioritize stop-level risk assessment.

**TripGuardian addresses this gap** by providing a predictive score that highlights which bus stops may require closer inspection or preventive work—empowering agencies like RTD to improve service quality and rider safety.

---

## Features

-  **Crime-Aware Spatial Analysis** using historical incident data
-  **Schedule Pressure Scoring** based on GTFS stop_times frequency
-  **Risk Modeling** that outputs a 0–1 score per stop
-  **Modular Codebase** organized for clarity and scalability
-  **Ready for integration** into dashboards or API endpoints

---

## Project Structure

```
TripGuardian/
├── data/                        # GTFS feeds, crime logs, etc.
├── notebooks/                  # Exploratory Jupyter Notebooks
├── models/                     # Trained models (optional)
├── src/
│   ├── core/                   # Core business logic
│   │   ├── scoring.py
│   │   ├── spatial.py
│   │   └── schedule.py
│   ├── io/                     # File I/O utilities
│   │   ├── reader.py
│   │   └── writer.py
│   ├── utils/                  # Merging, normalization, etc.
│   │   └── merge.py
│   └── pipeline/               # Main script
│       └── run_model.py
├── deprecated/                 # Legacy versions of files
├── requirements.txt
├── README.md
└── maintenance_risk_scores.csv
```

---

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the pipeline

```bash
python src/pipeline/run_model.py
```

This will generate:

```
✅ Risk scores written to maintenance_risk_scores.csv
```

---

## 📊 Output Example

| stop_id | crime_score | schedule_score | risk_score |
|---------|-------------|----------------|------------|
| 26175   | 0.85        | 0.62           | 0.748      |
| 33290   | 1.00        | 0.77           | 0.862      |
| 12522   | 0.12        | 0.43           | 0.246      |

---

## Methodology

- Crimes near a stop are counted using `scipy.spatial.cKDTree` within a 100m radius.
- Stop usage frequency is derived from `stop_times.txt` and normalized.
- A weighted score combines both using a default ratio of 60% crime, 40% schedule pressure.

---

## Use Cases

- RTD maintenance planning and prioritization
- Route rerouting decisions during high-risk events
- Future rider-facing dashboards showing stop reliability

---

## User Persona: Lisa (RTD Commuter)
- Age: 31
- Location: Englewood, CO
- Commutes daily to Union Station
- Prefers routes with fewer transfers and safe stops
- Uses RTD trip planner to check delays
- Wants to avoid buses that are packed

---


## Hackathon Rubric Alignment

| Category                | Strengths                                                                 |
|------------------------|---------------------------------------------------------------------------|
| Problem & Solution     | Clearly defined urban transit risk scenario                              |
| Impact & Feasibility   | RTD data, real-world relevance, scalable to other cities                  |
| Technical Depth        | Spatial KDTree, data normalization, modular design                        |
| Innovation & Creativity| Combining public safety + transit planning in a novel way                |
| Q&A Preparation        | Logic is defensible and easy to explain                                  |
| Presentation & Clarity | Code and CSV outputs are clean and communicable                          |
| User-Centered Design   | Designed for RTD and urban agencies, expandable to riders                |

---

## Submission Requirements

- GitHub Repo: [YourRepoLinkHere]
- Final Slide Deck: [Google Slides or OneDrive Share Link]
- Output File: `maintenance_risk_scores.csv`

---

## Contact

*Author:* Christian Mandujano Borjas  
*Email:* Christian.Mandujano.Borjas@gmail.com  
*Affiliation:* University of Colorado Denver – Hackathon 2025

---