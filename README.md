# IMF GADGET DESIGN

## Features
- Secure authentication using OAuth2
- CRUD operations for gadgets
- PostgreSQL database integration
- Proper error handling with validation
- Deployed on Render

## Tech Stack
- FastAPI as the backend framework
- PostgreSQL for database storage
- OAuth2 for authentication
- Render for deployment

## Installation
    1. Clone the repository:

       git clone https://github.com/sairamsreejith0/GadgetDesignAPI.git

    2) cd your_repo
    3) python -m venv venv 
    4) venv\Scripts\activate
    5) Install dependencies - pip install -r requirements.txt
    6) Setup .env 
       DATABASE_URL=postgresql://username:password@hostname:port/database  
       SECRET_KEY=your-secret-key  
       ALGORITHM=HS256  
       ACCESS_TOKEN_EXPIRE_MINUTES=30  
    7) Start FastAPI Server 
       uvicorn app.main:app --reload
    8) Swagger UI - http://127.0.0.1:8000/docs - access this url to test the API
    9) First access /auth/register to register the user
    10) Login using /auth/token
    11) Now access the API endpoints


Deployment link : https://gadgetdesignapi.onrender.com/docs

    
