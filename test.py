# schemas.py
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import uuid

class RuleEvaluationDetailsSchema(BaseModel):
    rule_id: str
    rule_desc: str
    rule_evaluation_status: str

class PolicyEngineResponseSchema(BaseModel):
    rule_evaluation_details: List[RuleEvaluationDetailsSchema]
    policy_evaluation_status: str
    policy_version: str

class BusinessApplicationDetailsSchema(BaseModel):
    source_itam_id: str
    source_application_status: str
    source_business_criticality: str
    destination_itam_id: str
    destination_application_status: str
    destination_business_criticality: str

class FirewallPolicyRequestCreateSchema(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request: Dict[str, Any]
    status: str
    response: Optional[Dict[str, Any]]
    response_status_code: Optional[int]
    business_application_details: BusinessApplicationDetailsSchema
    policy_engine_response: PolicyEngineResponseSchema
    created_by: Optional[str]
    updated_by: Optional[str]

class FirewallPolicyRequestUpdateSchema(BaseModel):
    request: Optional[Dict[str, Any]]
    status: Optional[str]
    response: Optional[Dict[str, Any]]
    response_status_code: Optional[int]
    business_application_details: Optional[BusinessApplicationDetailsSchema]
    policy_engine_response: Optional[PolicyEngineResponseSchema]
    updated_by: Optional[str]
    
    
# crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from models import FirewallPolicyRequests
from schemas import FirewallPolicyRequestCreateSchema, FirewallPolicyRequestUpdateSchema
from sqlalchemy.future import select

async def create_firewall_policy_request(db: AsyncSession, request: FirewallPolicyRequestCreateSchema):
    firewall_request = FirewallPolicyRequests(
        request_id=request.request_id,
        request=request.request,
        status=request.status,
        response=request.response,
        response_status_code=request.response_status_code,
        business_application_details=request.business_application_details.dict(),
        policy_engine_response=request.policy_engine_response.dict(),
        created_by=request.created_by,
        updated_by=request.updated_by,
    )
    db.add(firewall_request)
    await db.commit()
    await db.refresh(firewall_request)
    return firewall_request

async def update_firewall_policy_request(db: AsyncSession, request_id: str, request: FirewallPolicyRequestUpdateSchema):
    stmt = select(FirewallPolicyRequests).where(FirewallPolicyRequests.request_id == request_id)
    result = await db.execute(stmt)
    firewall_request = result.scalar_one_or_none()

    if not firewall_request:
        return None

    if request.request:
        firewall_request.request = request.request
    if request.status:
        firewall_request.status = request.status
    if request.response:
        firewall_request.response = request.response
    if request.response_status_code:
        firewall_request.response_status_code = request.response_status_code

    if request.business_application_details:
        firewall_request.business_application_details = request.business_application_details.dict()

    if request.policy_engine_response:
        firewall_request.policy_engine_response = request.policy_engine_response.dict()

    if request.updated_by:
        firewall_request.updated_by = request.updated_by

    await db.commit()
    await db.refresh(firewall_request)
    return firewall_request
