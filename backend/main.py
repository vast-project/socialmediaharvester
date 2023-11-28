#!/usr/bin/env python3
"""A web service for managing social network surveys and responses.
This was developed at [ISLab](https://islab.di.unimi.it) as part of the [VAST Project](https://www.vast-project.eu/)
Supports open and closed questioning, also with images when needed.

Use [HTTP Basic Auth](https://stackoverflow.com/a/50528734/1827854) username to identify user on Twitter.
The corresponding password is ignored."""
from typing import Dict, Optional

import shutil

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

# from sql_app import persistence, models, twitter_client
# from sql_app.database import SessionLocal, engine
from settings import VERSION, MEDIA_DIR
from router import post, fetch, identity  # , settings

# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IslabTweet",
    description=__doc__,
    docs_url="/",
    version=VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # needed for Basic Auth
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router, tags=["Post"], prefix="/post")
app.include_router(fetch.router, tags=["Fetch"], prefix="/fetch")
app.include_router(identity.router, tags=["Identity"], prefix="/identity")
# Disable access to settings/secrets for security reasons.
# Also disabling user management, since currently not required for access
# Both should be re-enabled whenever authentication mechanism is introduced.
# see https://fastapi.tiangolo.com/advanced/security/http-basic-auth/
# app.include_router(settings.router, tags=['Settings'], prefix='/settings')
# app.include_router(identity.router, tags=['Identity'], prefix='/identity')

# https://fastapi.tiangolo.com/tutorial/bigger-applications/


@app.post("/media")
async def upload_image(file: Optional[UploadFile] = None) -> Dict[str, str]:
    """Upload a single file. Responds with the file path the way it needs to be passed to the post endpoint."""
    if not file:
        return {"error": "No upload file sent"}
    perm_name = f"{MEDIA_DIR}/{file.filename}"
    with open(perm_name, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"filename": perm_name}


if __name__ == "__main__":
    import uvicorn  # type: ignore

    uvicorn.run("main:app", reload=True)
