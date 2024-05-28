from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Request
from firebase_admin import auth

security = HTTPBearer()


async def verify_firebase_token(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        decoded_token = auth.verify_id_token(credentials.credentials)
        request.state.user_data = decoded_token
        return decoded_token
    except auth.InvalidIdTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Firebase token: {str(e)}",
        )
