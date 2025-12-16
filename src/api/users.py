from fastapi import APIRouter, Response, HTTPException, Depends

# from src.main import security, config
from src.schemas.users import UserLogitSchema
from authx import AuthX, AuthXConfig

router = APIRouter()

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)



@router.post("/login",tags=["Пользователь👨🏻‍"])
def login(creads: UserLogitSchema, response: Response):
    if creads.username == "test" and creads.password == "test":
        token = security.create_access_token(uid="12345")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Incorrect username or password")


@router.get("/protected",
         tags=["Пользователь👨🏻‍"],
         dependencies=[Depends(security.access_token_required)]
         )
def get_protected():
    return {"message": "Hello World"}