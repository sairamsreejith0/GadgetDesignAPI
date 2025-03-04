**IMF GADGET DESIGN**
A FastAPI-based project that provides CRUD operations for managing gadgets, including authentication, authorization, and robust error handling.
Features
Secure authentication using OAuth2
    CRUD operations for gadgets
    PostgreSQL database integration
    Proper error handling with validation
    Deployed on Render

Tech Stack
    FastAPI as the backend framework for building scalable and high-performance APIs.
    PostgreSQL for database storage, ensuring structured and reliable data management.
    OAuth2 authentication for secure user access control.
    Render for deployment, making the API publicly accessible.

Installation 
    1) git clone https://github.com/sairamsreejith0/GadgetDesignAPI.git
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

    
