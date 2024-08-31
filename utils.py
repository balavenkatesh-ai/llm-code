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