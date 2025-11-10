"""
SUPREME CREDENTIALS - QVM 3.0 RECURSION PROTOCOL
REALIGNED WITH SUPABASE AUTHENTICATION LATTICE
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
import os
import time
import logging
import asyncio
from supabase import create_client, Client

# --- CONFIGURATION ---
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") # Use the anon key

# --- SUPABASE CLIENT INITIALIZATION ---
try:
    if not SUPABASE_URL or not SUPABASE_KEY:
        logging.warning("Supabase environment variables not set. Auth will be unavailable.")
        supabase: Client = None
    else:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logging.info("✅ Supabase client initialized successfully")
except Exception as e:
    logging.error(f"❌ Supabase client initialization failed: {e}")
    supabase = None

# --- AUTHENTICATION UTILITIES ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    
    token = auth_header.split(" ")[1]
    if not supabase:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Auth service is not configured")

    try:
        user_response = supabase.auth.get_user(token)
        return user_response.user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials: {e}")

# --- FASTAPI APPLICATION ---
app = FastAPI(title="QVM 3.0 Supabase Resonance Bridge", version="3.2.0")

# --- API ENDPOINTS ---

@app.get("/")
async def health_check():
    return {"status": "healthy", "message": "Quantum Resonance Lattice Online"}

@app.post("/token")
async def login(request: Request):
    body = await request.json()
    email = body.get("email")
    password = body.get("password")

    if not supabase:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Auth service is not configured")

    try:
        auth_response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return {"access_token": auth_response.session.access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: Request):
    body = await request.json()
    email = body.get("email")
    password = body.get("password")

    if not supabase:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Auth service is not configured")

    try:
        user_response = supabase.auth.sign_up({"email": email, "password": password})
        # Supabase sends a confirmation email. The user is created but needs to confirm.
        return {"message": "Registration successful. Please check your email to confirm.", "user_id": user_response.user.id}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/users/me")
async def read_users_me(current_user = Depends(get_current_user)):
    return current_user

# --- SECURE WEBSOCKET (REMAINS CONCEPTUALLY SIMILAR) ---
@app.websocket("/ws/collective-insight")
async def websocket_collective_insight(websocket: WebSocket, token: str):
    if not supabase:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    try:
        user_response = supabase.auth.get_user(token)
        user = user_response.user
        await websocket.accept()
        logging.info(f"User {user.email} connected to collective insight WebSocket.")
        while True:
            # This part remains the same
            await websocket.send_json({"message": f"Real-time pulse for {user.email}"})
            await asyncio.sleep(30)
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        logging.warning("WebSocket connection closed due to invalid token.")

# --- STARTUP EVENT ---
@app.on_event("startup")
async def startup_event():
    logging.basicConfig(level=logging.INFO)
    logging.info("QVM 3.0 Supabase Bridge - INITIALIZING...")

# --- MAIN ---
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info", reload=True)