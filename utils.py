from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional, List

app = FastAPI()

# Response structure model
class APIResponse(BaseModel):
    data: Optional[Any] = None
    message: str
    status_code: int

@app.get("/tip/component_details", summary="Get TIP Component details by GTS ID or Component Name")
async def get_tip_gts_by_gts_id(
    gts_id: Optional[str] = Query(None, description="GTS ID to filter the components"),
    component_name: Optional[str] = Query(None, description="Component name to filter the components"),
    db_session: Session = Depends(get_db_session)
):
    """
    Retrieve TIP component details by either GTS ID or Component Name.
    At least one of them is required.
    """
    try:
        result = get_tip_gts_by_gts_id_logic(gts_id, component_name, db_session)
        if not result:
            return JSONResponse(status_code=404, content=APIResponse(
                data=None, message="No records found", status_code=404).dict())
        
        return JSONResponse(status_code=200, content=APIResponse(
            data=result, message="Success", status_code=200).dict())
    
    except ValueError as e:
        return JSONResponse(status_code=400, content=APIResponse(
            data=None, message=str(e), status_code=400).dict())
    except Exception as e:
        return JSONResponse(status_code=500, content=APIResponse(
            data=None, message=f"An error occurred: {e}", status_code=500).dict())

def get_tip_gts_by_gts_id_logic(gts_id: Optional[str], component_name: Optional[str], db_session) -> List[TipGts]:
    query = db_session.query(TipGts)

    if gts_id:
        query = query.filter(TipGts.gts_id == gts_id)
    elif component_name:
        query = query.filter(TipGts.component_name == component_name)
    else:
        raise ValueError("Either 'gts_id' or 'component_name' must be provided")

    return query.all()