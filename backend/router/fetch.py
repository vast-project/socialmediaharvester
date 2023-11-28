"""Web service endpoints responsible for inserting pre-existing post"""
from fastapi import Depends, APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from sql_app import social


router = APIRouter()
security = HTTPBasic()


@router.get("/{id_on_network}")
async def get_post(
    id_on_network: str = "", credentials: HTTPBasicCredentials = Depends(security)
):
    """Get all posts managed by our users. This is different from getting the respective responses."""

    return social.get_post_from_netid(id_on_network, credentials.username)
