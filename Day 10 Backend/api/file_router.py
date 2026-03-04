from fastapi import APIRouter, Depends
from factories.file_factory import get_file_usecase
from usecases.file_usecase import FileUsecase
from security.oauth2 import oauth2_scheme

router = APIRouter(prefix="/files", tags=["files"])

@router.post("")

def create_upload_url(
    content_type: str,
    token: str = Depends(oauth2_scheme),
    usecase: FileUsecase = Depends(get_file_usecase)
):
    return usecase.generate_file_name(content_type)
