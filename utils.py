from sqlmodel import SQLModel, create_engine, Session, select

class TipControlRemediation(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    tip_gts_id: str
    tip_remediation_data: str
    tip_version: str
    active: bool

engine = create_engine("sqlite:///tip.db")
SQLModel.metadata.create_all(engine)

def insert_data():
    with Session(engine) as session:
        new_remediation = TipControlRemediation(
            tip_gts_id="12345",
            tip_remediation_data='{"key": "value"}',
            tip_version="1.0",
            active=True
        )
        session.add(new_remediation)
        session.commit()

def retrieve_data(tip_gts_id: str):
    with Session(engine) as session:
        statement = select(TipControlRemediation).where(TipControlRemediation.tip_gts_id == tip_gts_id)
        remediation = session.exec(statement).first()
        return remediation

insert_data()
result = retrieve_data("12345")
print(result.tip_remediation_data)

from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlalchemy.types import JSON
from typing import Optional

# Define the TipInventory model
class TipInventory(SQLModel, table=True):
    __tablename__ = "tip_inventory"  # Specify the table name
    
    id: Optional[int] = Field(default=None, primary_key=True)
    request_id: str = Field(nullable=False)
    build_id: Optional[int]
    ci_id: Optional[int]
    repo_name: Optional[str] = Field(max_length=100)
    project_name: Optional[str] = Field(max_length=100)
    branch: Optional[str] = Field(max_length=100)
    failed_results: Optional[dict] = Field(sa_column=Field(JSON))

# Define your database URL
DATABASE_URL = "sqlite:///tip_inventory.db"  # Replace with PostgreSQL URL when migrating

# Create the engine
engine = create_engine(DATABASE_URL)

# Create the table (if it doesn't exist)
SQLModel.metadata.create_all(engine)

def insert_tip_inventory(
    request_id: str, build_id: Optional[int], ci_id: Optional[int],
    repo_name: Optional[str], project_name: Optional[str],
    branch: Optional[str], failed_results: Optional[dict]
):
    """
    Inserts a new record into the TipInventory table.
    
    Args:
        request_id (str): Request ID.
        build_id (int, optional): Build ID.
        ci_id (int, optional): CI ID.
        repo_name (str, optional): Repository name.
        project_name (str, optional): Project name.
        branch (str, optional): Branch name.
        failed_results (dict, optional): Failed results as a JSON object.
    """
    try:
        with Session(engine) as session:
            new_tip = TipInventory(
                request_id=request_id,
                build_id=build_id,
                ci_id=ci_id,
                repo_name=repo_name,
                project_name=project_name,
                branch=branch,
                failed_results=failed_results
            )
            session.add(new_tip)
            session.commit()
            session.refresh(new_tip)
            print(f"Inserted TipInventory with ID: {new_tip.id}")
    except Exception as e:
        print(f"Error inserting TipInventory: {e}")
        
        def read_tip_inventory(request_id: str):
    """
    Retrieves records from the TipInventory table based on request_id.
    
    Args:
        request_id (str): The Request ID to filter by.
    
    Returns:
        list: A list of TipInventory records that match the request_id.
    """
    try:
        with Session(engine) as session:
            statement = select(TipInventory).where(TipInventory.request_id == request_id)
            results = session.exec(statement).all()
            return results
    except Exception as e:
        print(f"Error reading TipInventory: {e}")
        return []
