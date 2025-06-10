# Triage-ML

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [System Architecture](#system-architecture)
4. [Setup Instructions](#setup-instructions)
   - [Frontend Setup](#frontend-setup)
   - [Backend Setup](#backend-setup)
5. [Usage](#usage)
   - [Frontend](#frontend)
   - [Backend](#backend)
6. [API Endpoints](#api-endpoints)
   - [Authentication](#authentication)
   - [Patient Data](#patient-data)
7. [Deployment](#deployment)

---

## Overview

**Triage-ML** is a machine learning-powered emergency room triage assistant. It integrates with SMART on FHIR to retrieve patient medical data and uses rule-based or LLM-based strategies to calculate Emergency Severity Index (ESI) scores. The system provides explanations for the triage decisions and allows overrides by medical professionals.

---

## Features

- **Patient Data Retrieval**: Fetches patient demographics, vitals, conditions, medications, allergies, and clinical notes using SMART on FHIR.
- **Triage Scoring**: Calculates ESI scores using Large Language Models (LLMs) via OpenAI or similar APIs.
- **Interactive Frontend**: A React-based UI for entering patient data, viewing medical history, and overriding triage scores.
- **Backend API**: A FastAPI-based backend for handling data processing and scoring.
- **Logging and Error Handling**: Comprehensive logging and middleware for error handling.

---

## System Architecture

The system consists of two main components:

1. **Frontend**:
   - Built with React and TailwindCSS.
   - Handles user input, displays patient data, and communicates with the backend.

2. **Backend**:
   - Integrates with SMART on FHIR for patient data.
   - Implements scoring strategies (LLM-based).
   - Uses FHIRService to directly retrieve patient FHIR data from SMART sandbox.
   - Provides RESTful FastAPI as a wrapper for FHIRService to interact with the frontend.

---

## Setup Instructions

### Prerequisites

- **Frontend**:
  - Node.js (v16 or higher)
  - npm or yarn

- **Backend**:
  - Python (v3.9 or higher)
  - Virtual environment (optional)
  - `.env` file with required environment variables

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
2. Install dependencies:
    ```bash
    npm install
3. Start the development server:
    ```bash
    npm start
4. Open the app in your browser at http://localhost:3000.

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
4. Set up the `.env` file:
    Update the relevant environment variables if needed (`REDIRECT_URI`, `OPENAI_API_KEY`, `BASE_URL`, `FRONTEND_URL`).
5. Run the backend server
    ```bash
    uvicorn app.main:app --reload
6. Navigate to https://launch.smarthealthit.org/ in your web browser and enter in the URL of {`BASE_URL`}/auth/launch and click Launch.
7. Select an arbitrary patient on the "Select Patient" screen in order to generate a Bearer token.

### Usage
#### Frontend
1. Enter patient details in the Patient Input Form.
2. View the patient's medical history and triage score.
3. Override the triage score if necessary.
4. Submit the triage decision.
#### Backend
- Use the API endpoints to fetch patient data, calculate triage scores, and retrieve medical history using our FastAPI backend
- Example API call to fetch patient demographics (patient_id can be retrieved in response from "Select Patient" screen):
    ```bash
    curl -X GET "http://localhost:8000/api/v1/patient/{patient_id}/demographics"

### API Endpoints / Methods
#### Authentication
- `GET /auth/login`: Initiates SMART on FHIR login
- `GET /auth/launch`: Launches SMART on FHIR context
- `GET /auth/callback`: Handles OAuth2 callback and generates Bearer token.
#### Patient Data 
##### Key FastAPI Endpoints
- `GET /api/v1/patient/{patient_id}`: Fetch patient details.
- `POST /api/v1/patient/medical-history`: Retrieve and consolidate structured summary of medical history from FHIRService.
##### Key FHIRService Methods
- `find_patient_id(first_name: str, last_name: str, dob: str)`:  
  Finds the patient ID based on the provided first name, last name, and date of birth.

- `get_patient_demographics(patient_id: str)`:  
  Retrieves the demographics of a patient, including name, birth date, gender, and other identifying information.

- `get_conditions(patient_id: str, clinical_status: Optional[str] = None)`:  
  Fetches the conditions/problems of a patient. Optionally filters by clinical status (e.g., active, resolved).

- `get_medications(patient_id: str)`:  
  Retrieves the list of medications prescribed to the patient, including dosage and timing details.

- `get_allergies(patient_id: str)`:  
  Retrieves the patient's allergies, including criticality and reactions.

- `get_clinical_notes(patient_id: str, fetch_content: bool = False)`:  
  Fetches clinical notes for the patient. If `fetch_content` is set to `True`, retrieves the full content of the notes.

- `get_encounters(patient_id: str)`:  
  Retrieves the patient's encounters, including type, class, reason, and time period.

##### Key LLM Scoring Method
- `score(self, data: LLMRequest)`:  
  Uses patient vitals, symptoms, and past medical history, sends it to an LLM for scoring, and calculates a score and provide an explanation.

## Deployment

The Triage-ML project is deployed using [Render](https://render.com/), a cloud platform for hosting web applications and APIs. Below are the steps and configuration details for deploying the frontend and backend.

### Backend Deployment Configuration

The backend is deployed on a personal Render account and the backend has automatically been deployed to the URL: https://triage-ml-backend.onrender.com.
Certain environment variables must be set in the deployed backend in Render in order to use the deployed stack.
- `BASE_URL`: https://triage-ml-backend.onrender.com
- `FRONTEND_URL`: https://triage-ml.onrender.com
- `REDIRECT_URI`: https://triage-ml-backend.onrender.com/auth/callback

### Frontend Deployment Configuration

The frontend is deployed on a personal Render account and the frontend has automatically been deployed to the URL: https://triage-ml.onrender.com.