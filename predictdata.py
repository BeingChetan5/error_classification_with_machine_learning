from pydantic import BaseModel

class PredictData(BaseModel):
    error_msg: str
