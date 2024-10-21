from sqlalchemy.orm import Session
from fastapi import HTTPException

def update_component_details(gts_id: str, update_data: UpdateComponentDetails, db_session: Session):
    # Fetch the tip_component_details record using gts_id
    tip_component_details = db_session.query(TipGts).filter(TipGts.gts_id == gts_id).one_or_none()

    if not tip_component_details:
        # If the record is not found, raise an HTTPException
        raise HTTPException(status_code=404, detail="tip_component_details record not found")

    # Update fields only if the data is provided (this ensures partial updates)
    if update_data.tip_availability is not None:
        tip_component_details.tip_availability = update_data.tip_availability
    if update_data.scanner_name is not None:
        tip_component_details.scanner_name = update_data.scanner_name
    if update_data.tip_component_name is not None:
        tip_component_details.tip_component_name = update_data.tip_component_name
    if update_data.config_file_mapping is not None:
        tip_component_details.config_file_mapping = update_data.config_file_mapping
    if update_data.control_id_mapping is not None:
        tip_component_details.control_id_mapping = update_data.control_id_mapping
    if update_data.unmapped_id_mapping is not None:
        tip_component_details.unmapped_id_mapping = update_data.unmapped_id_mapping
    if update_data.qualys_config is not None:
        tip_component_details.qualys_config = update_data.qualys_config

    # Commit the updates to the database
    db_session.commit()
    db_session.refresh(tip_component_details)

    # Return a success message with updated data
    return {
        "message": "Updated successfully",
        "tip_component_details": tip_component_details
    }
    
    
    from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class UpdateComponentDetails(BaseModel):
    tip_availability: Optional[str] = None
    scanner_name: Optional[str] = None
    tip_component_name: Optional[str] = None
    config_file_mapping: Optional[List[Dict[Any, Any]]] = None
    control_id_mapping: Optional[List[Dict[Any, Any]]] = None
    unmapped_id_mapping: Optional[List[Dict[Any, Any]]] = None
    qualys_config: Optional[List[Dict[Any, Any]]] = None

    class Config:
        orm_mode = True