from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional

# Define the TipInventory model
class TipInventory(SQLModel, table=True):
    __tablename__ = "tip_inventory"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    request_id: str = Field(nullable=False)
    status: Optional[str] = Field(max_length=50)  # Adding status column

# Initialize FastAPI app
app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///tip_inventory.db"
engine = create_engine(DATABASE_URL)

# Create the table (if it doesn't exist)
SQLModel.metadata.create_all(engine)

@app.patch("/tip-inventory/{tip_id}")
async def update_tip_inventory_status(tip_id: int, status: str):
    """
    PATCH endpoint to update the status of a TipInventory record.
    
    Args:
        tip_id (int): The ID of the TipInventory record to update.
        status (str): The new status value to set.
    
    Returns:
        dict: A success message or an error message.
    """
    try:
        with Session(engine) as session:
            statement = select(TipInventory).where(TipInventory.id == tip_id)
            tip_inventory = session.exec(statement).first()
            if not tip_inventory:
                raise HTTPException(status_code=404, detail="TipInventory record not found")
            
            # Update the status
            tip_inventory.status = status
            session.add(tip_inventory)
            session.commit()
            session.refresh(tip_inventory)
            
            return {"message": "Status updated successfully", "tip_inventory": tip_inventory}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating status: {str(e)}")