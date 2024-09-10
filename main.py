from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from .database import SessionLocal, engine

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
        print(db)
    except:
        print("An exception occured")
    finally:
        db.close()


@app.get('/health')
def get_health(db: Session = Depends(get_db)):
    return {"message", "connected"}
