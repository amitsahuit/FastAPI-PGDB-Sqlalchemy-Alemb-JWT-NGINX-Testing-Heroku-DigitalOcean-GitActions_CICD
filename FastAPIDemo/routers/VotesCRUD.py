from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import mode
from .. import models, Schemas, Database, oAuth2


router = APIRouter(
    prefix="/vote", tags= ['VOTES']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def postAVote(vote: Schemas.Vote, db: Session = Depends(Database.get_db), current_user: int = Depends(oAuth2.get_current_user)):
    
    #check if the vote alredy present?
    vote_query = db.query(models.Vote).filter(models.Vote.user_id==current_user.id, models.Vote.partner_id == vote.partner_id)
    found_vote = vote_query.first()
    
    if (vote.direction == 1): #If user like the partner
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted for paerner {vote.partner_id}")
        new_vote = models.Vote(partner_id = vote.partner_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"mesage":"Successfully added vote"}
    else: #If user dont like the partner
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"mesage":"successfully deleted vote."}