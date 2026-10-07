import os
import json
from datetime import datetime
from urllib.request import urlopen

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request, Depends
from jose import jwt
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.routers.auth import create_access_token


load_dotenv(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        ".env"
    )
)


router = APIRouter(
    prefix="/auth0",
    tags=["Auth0"]
)


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")

AUTH0_CALLBACK_URL = os.getenv(
    "AUTH0_CALLBACK_URL",
    "http://127.0.0.1:8001/auth0/callback"
)


oauth = OAuth()

oauth.register(
    name="auth0",
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    server_metadata_url=(
        f"https://{AUTH0_DOMAIN}"
        "/.well-known/openid-configuration"
    ),
    client_kwargs={
        "scope": "openid profile email"
    },
)


@router.get("/login")
async def auth0_login(request: Request):

    if not AUTH0_DOMAIN or not AUTH0_CLIENT_ID:
        raise HTTPException(
            status_code=500,
            detail="Auth0 configuration is missing"
        )

    return await oauth.auth0.authorize_redirect(
        request,
        AUTH0_CALLBACK_URL
    )


@router.get("/callback")
async def auth0_callback(
    request: Request,
    db: Session = Depends(get_db)
):

    try:
        token = await oauth.auth0.authorize_access_token(request)

        userinfo = token.get("userinfo", {})

        email = userinfo.get("email")
        name = userinfo.get("name") or email

        if not email:
            raise HTTPException(
                status_code=400,
                detail="Email not provided by Auth0"
            )

        user = db.query(User).filter(
            User.email == email
        ).first()

        if not user:
            user = User(
                name=name,
                email=email,
                password="AUTH0_USER",
                role="customer",
                date_joined=datetime.now()
            )

            db.add(user)
            db.commit()
            db.refresh(user)

        access_token = create_access_token(
            user_id=user.id,
            email=user.email,
            role=user.role
        )

        return {
            "message": "Auth0 login successful",
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "picture": userinfo.get("picture")
            }
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Auth0 login failed: {str(e)}"
        )


@router.post("/verify")
def verify_auth0_token(token: str):

    if not AUTH0_DOMAIN or not AUTH0_AUDIENCE:
        raise HTTPException(
            status_code=500,
            detail="Auth0 configuration is missing"
        )

    try:
        jwks_url = (
            f"https://{AUTH0_DOMAIN}"
            "/.well-known/jwks.json"
        )

        with urlopen(jwks_url) as response:
            jwks = json.loads(
                response.read()
            )

        unverified_header = jwt.get_unverified_header(
            token
        )

        rsa_key = {}

        for key in jwks["keys"]:

            if key["kid"] == unverified_header["kid"]:

                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }

                break

        if not rsa_key:
            raise HTTPException(
                status_code=401,
                detail="Unable to find signing key"
            )

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=AUTH0_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/",
        )

        return {
            "message": "Auth0 token verified successfully",
            "user": payload,
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid Auth0 token: {str(e)}"
        )