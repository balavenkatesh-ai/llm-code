
from enum import Enum
from pydantic import BaseModel, Field
from typing import List

class Action(str, Enum):
    permit = "permit"
    deny = "deny"

class Rule(str, Enum):
    add = "add"
    remove = "remove"

class Pipeline(BaseModel):
    repo_name: str
    build_id: str
    ado_env: str

class FirewallDetails(BaseModel):
    src_address: str
    dst_address: str
    dst_port: int
    action: Action
    rule: Rule

class FirewallRequest(BaseModel):
    itam_id: str
    dst_id: str
    pipeline: Pipeline
    firewall_details: List[FirewallDetails]