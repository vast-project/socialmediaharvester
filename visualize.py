#!/usr/bin/env python3

from sqlalchemy import schema  # type: ignore
from eralchemy2 import render_er

from sql_app.database import engine, Base

# schema_name = 'socialcampaigns'
# if not engine.dialect.has_schema(engine, schema_name):
#     engine.execute(schema.CreateSchema(schema_name))

Base.metadata.create_all(bind=engine)
# db = SessionLocal()
# db.commit()
# db.close()

render_er(Base.metadata, "models.png")
