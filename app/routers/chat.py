from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db
from app import models, schemas
from app.rag.chat_chain import get_answer

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/", response_model=schemas.ChatResponse)
def chat(request: schemas.ChatRequest, db: Session = Depends(get_db)):
    session = db.query(models.ChatSession).filter(models.ChatSession.id == request.session_id).first()
    if not session:
        session = models.ChatSession(id=request.session_id)
        db.add(session)
        db.commit()

    history_rows = (
        db.query(models.ChatTurn)
        .filter(models.ChatTurn.session_id == request.session_id)
        .order_by(desc(models.ChatTurn.created_at))
        .limit(5)
        .all()
    )
    history = [{"query": t.query, "answer": t.answer} for t in reversed(history_rows)]

    result = get_answer(request.query, history)

    turn = models.ChatTurn(
        session_id=request.session_id,
        query=request.query,
        answer=result["answer"],
        confidence=result["confidence"],
        escalated=result["escalated"],
    )
    db.add(turn)

    if result["escalated"]:
        unresolved = models.UnresolvedQuery(
            session_id=request.session_id,
            query=request.query,
            confidence=result["confidence"],
        )
        db.add(unresolved)

    db.commit()
    return result