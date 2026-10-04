from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import schemas, crud, database
from app.database import get_db

router = APIRouter(prefix="/logs", tags=["logs"])

@router.post("/", response_model=schemas.OperationLogResponse)
def create_log(log: schemas.OperationLogCreate, db: Session = Depends(get_db)):
    return crud.create_log(db=db, log=log)


@router.get("/{log_id}", response_model=schemas.OperationLogResponse)
def get_log(log_id: int, db: Session = Depends(get_db)):
    db_log = crud.get_log(db=db, log_id=log_id)
    if not db_log:
        raise HTTPException(status_code=404, detail="Log not found")
    return db_log


@router.get("/", response_model=list[schemas.OperationLogResponse])
def get_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    user_id: int | None = None,
    target_table: str | None = None,
    action: str | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_logs(
        db=db,
        skip=skip,
        limit=limit,
        user_id=user_id,
        target_table=target_table,
        action=action,
    )


@router.delete("/{log_id}")
def delete_log(log_id: int, db: Session = Depends(get_db)):
    result = crud.delete_log(db=db, log_id=log_id)
    if not result:
        raise HTTPException(status_code=404, detail="Log not found")
    return {"detail": "Deleted"}