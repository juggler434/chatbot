from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
        print(db)
    except Exception:
        raise HTTPException(
                status_code=500, detail="Failed to get DB Connection"
                )
        print("An exception occured")
    finally:
        db.close()


@app.get('/health')
def get_health(db: Session = Depends(get_db)):
    return {"message", "connected"}
