from fastapi import APIRouter
from fastapi.params import Body
from typing import Optional
from .. import models,Schemas

router = APIRouter(
    prefix='/items', tags= ['ITEMS']
)

@router.get("/{item_id}")
async def read_item(item_id: int):
    return item_id

# @router.post("/createposts")
# def postMessage(payload: dict = Body(...)):
#     print(payload)
#     return {"new post":f"title{payload['title']}"}

@router.post("/")
def itemRequestMethod(item : Schemas.Item):
    name_dict=item.dict()
    if item.last_name:
        name_dict= item.first_name+" "+item.last_name
        return name_dict
    return name_dict

# @router.put("/{item_id}")
# def create_item(item_id: int, item:Item):
#     return {"item_id is ": item_id,**item.dict()}

@router.put("/{item_id}")
def create_item(item_id: int, Marital_status: bool, kids_count: int, item: Schemas.Item, q: Optional[str]=None):
    result={"item_id": item_id, "Marital_status": Marital_status, "kids_count": kids_count, **item.dict()}
    print(result)
    if q:
        result.update({"q value": q})
    return result
