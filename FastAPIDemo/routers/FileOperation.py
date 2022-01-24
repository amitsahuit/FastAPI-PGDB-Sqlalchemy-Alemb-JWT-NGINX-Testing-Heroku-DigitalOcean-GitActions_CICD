from fastapi import APIRouter, File, UploadFile

router = APIRouter(tags=['FILEOPERATIONS'])


@router.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}