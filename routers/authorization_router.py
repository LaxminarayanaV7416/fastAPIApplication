from fastapi import (
        APIRouter, 
        HTTPException, 
        status,
        Depends
    )
from fastapi.security import ( 
        OAuth2PasswordRequestForm
    )
from schema_models.login_schema_models import (
        LoginResponseSchema,
        RegisterRequestSchema,
        CurrentUserSchema
    )
from database_models.users_models import Users
from utilities.data_base_connectivity_utils import SingletonDataBaseConnectivitySQLIte
from utilities.authorisation_util import HashingJose, AccessTokenGenerator, get_current_user


router = APIRouter(
    tags = ["Authorization"]
)


@router.post("/register", response_model=CurrentUserSchema)
async def register(request: RegisterRequestSchema):
    email = request.email
    unhashed_password = request.password
    if email is None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
                            detail="please pass proper email for creation")
    if unhashed_password is None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
                            detail="please pass proper password for creation")
    # hash the password
    hashed_password = HashingJose().get_password_hash(unhashed_password)
    try:
        user = Users(email = email, password = hashed_password)
        session = SingletonDataBaseConnectivitySQLIte.get_session()
        session.add(user)
        session.commit()
        session.close()
    except Exception as err:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
                            detail=f"creation of user failed with error {err}")
    return CurrentUserSchema(email = email)


@router.post("/login", response_model = LoginResponseSchema)
async def login_method(request:OAuth2PasswordRequestForm = Depends()):
    # verify the user exsists or not intially
    session = SingletonDataBaseConnectivitySQLIte.get_session()
    user = session.query(Users).filter(Users.email == request.username).first()
    if user:
        # so user exsists here now check the password
        hash_confirmation = HashingJose().verify_password(request.password, user.password)
        if hash_confirmation:
            access_token = AccessTokenGenerator.create_access_token({"user" : user.email})
            return LoginResponseSchema(access_token=access_token, token_type="Bearer")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Incorrect Password",
                            headers={"WWW-Authenticate": "Bearer"})    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                        detail=f"No user found with email {request.email}",
                        headers={"WWW-Authenticate": "Bearer"})


@router.get("/test_login")
async def test(token: CurrentUserSchema = Depends(get_current_user)):
    return True