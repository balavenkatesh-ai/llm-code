# Import statements
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import datetime

# Assuming these are defined elsewhere
from .database import get_db_session, engine
from .models import TipControlRemediation
from . import app_constants

# Pydantic models
class TipControlRemediationBase(BaseModel):
    tip_gts_id: str
    remediation_data: dict
    tip_version: str
    active: bool = True

class TipControlRemediationCreate(TipControlRemediationBase):
    pass

class TipControlRemediationUpdate(BaseModel):
    remediation_data: Optional[dict] = None
    tip_version: Optional[str] = None
    active: Optional[bool] = None

class TipControlRemediationResponse(TipControlRemediationBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True

# Router
api_router = APIRouter()

# POST endpoint
@api_router.post(
    "/tip/control-remediation",
    response_model=TipControlRemediationResponse,
    summary="Create New TIP Control Remediation",
    tags=[app_constants.APIDocs.TIP_CONTROL_REMEDIATION],
)
async def create_tip_control_remediation(
    remediation: TipControlRemediationCreate,
    db: Session = Depends(get_db_session)
):
    return await save_to_remediation_table(remediation, db)

# PATCH endpoint
@api_router.patch(
    "/tip/control-remediation/{tip_gts_id}",
    response_model=TipControlRemediationResponse,
    summary="Update TIP Control Remediation",
    tags=[app_constants.APIDocs.TIP_CONTROL_REMEDIATION],
)
async def update_tip_control_remediation(
    tip_gts_id: str,
    remediation: TipControlRemediationUpdate,
    db: Session = Depends(get_db_session)
):
    return await update_remediation_table(tip_gts_id, remediation, db)

# Database operations
async def save_to_remediation_table(remediation: TipControlRemediationCreate, db: Session) -> TipControlRemediation:
    """
    Save the TIP Control Remediation data to the database.
    """
    try:
        db_remediation = TipControlRemediation(**remediation.dict())
        db.add(db_remediation)
        db.commit()
        db.refresh(db_remediation)
        return db_remediation
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving data: {str(e)}")

async def update_remediation_table(tip_gts_id: str, remediation: TipControlRemediationUpdate, db: Session) -> TipControlRemediation:
    """
    Update the TIP Control Remediation data in the database.
    """
    try:
        db_remediation = db.query(TipControlRemediation).filter(TipControlRemediation.tip_gts_id == tip_gts_id).first()
        if not db_remediation:
            raise HTTPException(status_code=404, detail="TIP Control Remediation not found")
        
        update_data = remediation.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_remediation, key, value)
        
        db_remediation.updated_at = datetime.datetime.utcnow()
        db.commit()
        db.refresh(db_remediation)
        return db_remediation
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating data: {str(e)}")

# Assuming you have a SQLAlchemy model defined like this:
# class TipControlRemediation(Base):
#     __tablename__ = "tip_control_remediation"
#
#     id = Column(Integer, primary_key=True, index=True)
#     tip_gts_id = Column(String, unique=True, index=True)
#     remediation_data = Column(JSON)
#     tip_version = Column(String)
#     active = Column(Boolean, default=True)
#     created_at = Column(DateTime, default=datetime.datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


@api_router.post(
    "/tip/control-remediation",
    summary="Create New TIP Control Remediation",
    tags=[app_constants.APIDocs.TIP_CONTROL_REMEDIATION],
    responses={200: {"message": "TIP Control Remediation Successfully Created in the Database"}}
)
async def save_tip_control_remediation(
    remediation_request: tip_control_remediation.TipControlRemediationRequest,
    db_session: Session = Depends(get_db_session)
):
    """Create New TIP Control Remediation"""
    try:
        await tip_control_remediation.save_to_remediation_table(remediation_request)
        return {"message": "TIP Control Remediation Successfully Created in the Database"}
    except Exception as e:
        return {"message": str(e)}
```

Now, let's implement the `save_to_remediation_table` function:

```python
async def save_to_remediation_table(remediation_request: TipControlRemediationRequest) -> None:
    """
    Save the TIP Control Remediation data to the database.

    :param remediation_request: The TIP Control Remediation request containing remediation details.
    """
    try:
        with Session(engine) as session:
            tip_remediation_data = TipControlRemediation(
                request_id=str(correlation_id.get()),
                tip_gts_id=remediation_request.tip_gts_id,
                remediation_data=remediation_request.remediation_data,
                tip_version=remediation_request.tip_version,
                active=remediation_request.active
            )
            session.add(tip_remediation_data)
            session.commit()
        print("Successfully saved data into tip_control_remediation table")
    except Exception as e:
        print(f"Error on saving into tip_control_remediation table: {e}")
        raise
```

For the patch endpoint, we can create a similar structure:

```python
@api_router.patch(
    "/tip/control-remediation/{tip_gts_id}",
    summary="Update TIP Control Remediation",
    tags=[app_constants.APIDocs.TIP_CONTROL_REMEDIATION],
    responses={200: {"message": "TIP Control Remediation Successfully Updated in the Database"}}
)
async def update_tip_control_remediation(
    tip_gts_id: str,
    remediation_request: tip_control_remediation.TipControlRemediationUpdateRequest,
    db_session: Session = Depends(get_db_session)
):
    """Update TIP Control Remediation"""
    try:
        await tip_control_remediation.update_remediation_table(tip_gts_id, remediation_request)
        return {"message": "TIP Control Remediation Successfully Updated in the Database"}
    except Exception as e:
        return {"message": str(e)}
```

And the corresponding `update_remediation_table` function:

```python
async def update_remediation_table(tip_gts_id: str, remediation_request: TipControlRemediationUpdateRequest) -> None:
    """
    Update the TIP Control Remediation data in the database.

    :param tip_gts_id: The ID of the TIP Control Remediation to update.
    :param remediation_request: The TIP Control Remediation request containing updated remediation details.
    """
    try:
        with Session(engine) as session:
            tip_remediation_data = session.query(TipControlRemediation).filter_by(tip_gts_id=tip_gts_id).first()
            if tip_remediation_data:
                tip_remediation_data.remediation_data = remediation_request.remediation_data
                tip_remediation_data.tip_version = remediation_request.tip_version
                tip_remediation_data.active = remediation_request.active
                session.commit()
                print(f"Successfully updated data in tip_control_remediation table for tip_gts_id: {tip_gts_id}")
            else:
                raise Exception(f"No TIP Control Remediation found for tip_gts_id: {tip_gts_id}")
    except Exception as e:
        print(f"Error on updating tip_control_remediation table: {e}")
        raise
```



Good day!

Firstly, I want to express how grateful I am to be a part of the TIP Squad, and especially to be part of Arun’s team. I truly appreciate both of you for your guidance and support throughout my journey here.

When I first onboarded to the TIP team, Bhuvi and Rafi were instrumental in helping me understand the TIP workflow, and from there, I was able to initiate the TIP API development independently. I am happy to share that we’ve successfully deployed it into staging. Moreover, as we discussed in our recent calls, I have more ideas to enhance the API development. For example, we could pass a configuration file to generate the PR description, with all the underlying operations handled by the API. This includes scanning and fixing misconfigurations automatically, either through the API or a UI, as per your suggestion.

Now, to address the specific points you outlined:

1, 2, 3, 6, 7 – These points emphasize learning new technologies, and I’m excited and open to acquiring new skills. However, before moving forward, I’d like to align these goals with my current skillset to ensure we are building on a solid foundation:

Python
API Development – FastAPI, Django, Flask
Databases – PostgreSQL, MySQL
Machine Learning
Deep Learning
Generative AI – LLM Models, Retrieval-Augmented Generation (RAG), Vector Databases
Frameworks – Langchain, LlamaIndex
I believe these skills will contribute to my quick adoption of any new technology necessary for the team.

Point 4: I am already taking ownership of API development, deployment, and IaC setup. I’m happy to continue taking responsibility for any new product initiatives, and as we discussed, I’m eager to contribute further to our API roadmap.

Point 5: I’m well-versed in AI/ML areas, and with sufficient hardware resources and datasets, I’m ready to start working on enhancing this area. It’s something I’m particularly excited about and ready to dive deeper into.

Point 8: I’ve already begun preparing myself to present tasks and ideas more professionally. Communication is a critical skill, and I’m continuously improving it. I’ve learned a great deal from the team, particularly through our 1:30 standup calls. I’m thankful for all the opportunities to grow alongside such talented colleagues.

One point I’d like to bring up that wasn’t discussed in our conversation:

Agile Methodology:
Currently, we aren't following Agile methodology effectively. While we do have some stories in the backlog, we are missing key elements such as sprint planning and retrospective meetings. However, I’m encouraged by Bhuvi’s assurance that in 2025, we’ll start adopting Agile practices more rigorously, including task assignments through ADO work items instead of verbal task allocation. This will bring numerous benefits, such as:

Implementing high-quality code with proper test cases based on acceptance criteria.
A clear understanding of requirements, allowing for stronger system designs.
Reducing the need for long daily standups and enabling more effective planning of ad-hoc tasks.
Avoiding last-minute rewrites by promoting proper line-by-line PR reviews and approvals.
I’m confident that with these improvements, you will see a "Bala Venkatesh 2.0" in 2025. I'm working diligently to align with these goals and contribute to the team's success.

Thank you once again for your continued support. I look forward to your feedback and any further guidance. And, of course, I would love to hear a few words from my first and foremost mentor, Arun!

Best regards,
Bala Venkatesh
