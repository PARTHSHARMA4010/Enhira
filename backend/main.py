from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select, SQLModel
from models import UserMaster
from db import engine, get_session
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("user-dashboard")

# Initialize FastAPI app
app = FastAPI(title="User Dashboard API")

# --- CORS Middleware for React Frontend --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite URL for React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------------------------------------------------

# --- Database Initialization on Startup ---------------------
@app.on_event("startup")
def on_startup() -> None:
    """
    Create all database tables on startup.
    """
    SQLModel.metadata.create_all(engine)
    logger.info("✅ Database tables created (if not already existing).")

# ---------- Health Check Endpoint ---------------------------
@app.get("/ping")
def ping():
    """
    Health check endpoint to verify backend is running.
    """
    logger.info("✅ Front-end just pinged the back-end")
    return {"status": "pong"}

# ---------- List Users Endpoint -----------------------------
@app.get("/users")
def list_users(session=Depends(get_session)):
    """
    Fetch all users from the database.
    """
    try:
        users = session.exec(select(UserMaster)).all()
        logger.info(f"📤 Sent {len(users)} user(s) to front-end")
        return users
    except Exception as e:
        logger.error(f"❌ Failed to fetch users: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch users")

# ---------- Create User Endpoint ----------------------------
# @app.post("/users")
# def create_user(user: UserMaster, session=Depends(get_session)):
#     """
#     Add a new user to the database.
#     """
#     try:
#         session.add(user)
#         session.commit()
#         session.refresh(user)
#         logger.info(f"➕ Added user {user.fullusername}")
#         return user
#     except Exception as e:
#         logger.error(f"❌ Failed to add user: {e}")
#         raise HTTPException(status_code=500, detail="Failed to add user")


@app.post("/users")
def create_user(user: UserMaster, session=Depends(get_session)):
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
        logger.info(f"➕ Added user {user.fullusername}")
        return user
    except Exception as e:
        logger.error(f"❌ Failed to add user: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to add user: {e}")




# ---------- Get User by ID Endpoint -------------------------
# @app.get("/users/{userid}")
# def get_user(userid: str, session=Depends(get_session)):
#     """
#     Fetch a specific user by their ID.
#     """
#     try:
#         user = session.get(UserMaster, userid)
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         logger.info(f"📤 Sent user {user.fullusername} to front-end")
#         return user
#     except Exception as e:
#         logger.error(f"❌ Failed to fetch user: {e}")
#         raise HTTPException(status_code=500, detail="Failed to fetch user")


@app.get("/users")
def list_users(session=Depends(get_session)):
    try:
        users = session.exec(select(UserMaster)).all()
        logger.info(f"📤 Sent {len(users)} user(s) to front-end")
        return users
    except Exception as e:
        logger.error(f"❌ Failed to fetch users: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch users: {e}")


# ---------- Update User Endpoint ----------------------------
@app.put("/users/{userid}")
def update_user(userid: str, updated_user: UserMaster, session=Depends(get_session)):
    """
    Update an existing user's details.
    """
    try:
        user = session.get(UserMaster, userid)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        for key, value in updated_user.dict(exclude_unset=True).items():
            setattr(user, key, value)
        session.add(user)
        session.commit()
        session.refresh(user)
        logger.info(f"✏️ Updated user {user.fullusername}")
        return user
    except Exception as e:
        logger.error(f"❌ Failed to update user: {e}")
        raise HTTPException(status_code=500, detail="Failed to update user")

# ---------- Delete User Endpoint ----------------------------
@app.delete("/users/{userid}")
def delete_user(userid: str, session=Depends(get_session)):
    """
    Delete a user from the database.
    """
    try:
        user = session.get(UserMaster, userid)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()
        logger.info(f"🗑️ Deleted user {user.fullusername}")
        return {"message": f"User {user.fullusername} deleted successfully"}
    except Exception as e:
        logger.error(f"❌ Failed to delete user: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete user")

# ---------- Run the Server -----------------------------------
# Command to run the server:
# uvicorn main:app --reload --port 8000
