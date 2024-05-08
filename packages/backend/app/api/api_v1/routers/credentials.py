from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from loguru import logger

# project imports
from app.db.session import get_db
from app.db.models import Credential
from app.api.api_v1.routers.schemes import CreateCredentialData, UpdateCredentialData
from app.core import security
from app.core.auth import get_current_active_user
from app.components.credentials import all_credentials

credential_routers = r = APIRouter()


# get all component credentials that can be saved
@r.get("/credentials/components")
async def get_all_credentials():
    """Get all possible credentials"""

    return [cred.model_dump() for _, cred in all_credentials.items()]


# get specific component credential by name
@r.get("/credentials/components/{name}")
async def get_credential(name: str):
    """Get a specific credential"""
    cred = all_credentials.get(name)

    if not cred:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Credential not found"
        )

    return cred.model_dump()


# return image for specific component credential
@r.get("/credentials/components/icon/{name}")
async def get_credential_icon(name: str):
    """Get a specific credential icon"""
    cred = all_credentials.get(name)

    if not cred:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Credential not found"
        )

    icon_path = cred.icon
    return FileResponse(icon_path) if icon_path else {"message": "No image found"}


# get all credentials for a user
@r.get("/credentials")
async def get_all_user_credentials(
    db=Depends(get_db), user=Depends(get_current_active_user)
):
    """Get all credentials for a user"""
    credentials = db.query(Credential).filter(Credential.user_id == user.id).all()

    return_data = []
    for credential in credentials:
        # decrypt the data
        decrypted_data = security.decrypt_json_data(credential.encrypted_data)

        return_data.append(
            {
                "id": credential.id,
                "name": credential.name,
                "credentialName": credential.credentialName,
                "credential": decrypted_data,
            }
        )

    return return_data


# create a new credential for a user
@r.post("/credentials/new")
async def new_user_credential(
    credeential_data: CreateCredentialData,
    db=Depends(get_db),
    user=Depends(get_current_active_user),
):
    """Save a new credential for a user"""

    if not credeential_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data"
        )

    # make sure user does not have credential with the same name
    existing_credential = (
        db.query(Credential)
        .filter(
            Credential.name == credeential_data.name,
            Credential.credentialName == credeential_data.credentialName,
            Credential.user_id == user.id,
        )
        .first()
    )

    if existing_credential:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Credential with the same name already exists for this user",
        )

    # encrypt the data
    encrypted_data = security.encrypt_json_data(credeential_data.credentialObj)

    # save the credential to the database
    db_credential = Credential(
        user_id=user.id,
        name=credeential_data.name,
        credentialName=credeential_data.credentialName,
        encrypted_data=encrypted_data,
    )
    db.add(db_credential)
    db.commit()
    db.refresh(db_credential)

    return {"id": db_credential.id, "credential": credeential_data.model_dump()}


# delete a user's credential
@r.delete("/credentials/{id}")
async def delete_user_credential(
    id: int, db=Depends(get_db), user=Depends(get_current_active_user)
):
    """Delete a user's credential"""
    db_credential = (
        db.query(Credential)
        .filter(Credential.id == id, Credential.user_id == user.id)
        .first()
    )
    db.delete(db_credential)
    db.commit()

    return {"message": "Credential deleted"}


# get a user's credential by id
@r.get("/credentials/{id}")
async def get_user_credential(
    id: int, db=Depends(get_db), user=Depends(get_current_active_user)
):
    """Get a single credential for a user"""
    credential = (
        db.query(Credential)
        .filter(Credential.id == id, Credential.user_id == user.id)
        .first()
    )

    if not credential:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Credential not found"
        )

    # decrypt the data
    decrypted_data = security.decrypt_json_data(credential.encrypted_data)

    return_data = {
        "id": credential.id,
        "name": credential.name,
        "credentialName": credential.credentialName,
        "credentialObj": decrypted_data,
    }

    return return_data


# get a user credential by list of credentialNames
@r.get("/credentials/names/{credentialNames}")
async def get_user_credentials_by_names(
    credentialNames: str, db=Depends(get_db), user=Depends(get_current_active_user)
):
    """Get a list of credentials for a user"""
    credential_names = credentialNames.split("&")

    credentials = (
        db.query(Credential)
        .filter(
            Credential.credentialName.in_(credential_names),
            Credential.user_id == user.id,
        )
        .all()
    )

    return_data = []
    for credential in credentials:
        # decrypt the data
        decrypted_data = security.decrypt_json_data(credential.encrypted_data)

        return_data.append(
            {
                "id": credential.id,
                "name": credential.name,
                "credentialName": credential.credentialName,
                "credentialObj": decrypted_data,
            }
        )

    return return_data


# update a user's credential
@r.put("/credentials/{id}")
async def update_user_credential(
    id: int,
    update_data: UpdateCredentialData,
    db=Depends(get_db),
    user=Depends(get_current_active_user),
):
    """Update a user's credential"""

    if not update_data or not update_data.credentialObj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data"
        )

    # encrypt the data
    encrypted_data = security.encrypt_json_data(update_data.credentialObj)

    # update the credential
    db_credential = (
        db.query(Credential)
        .filter(Credential.id == id, Credential.user_id == user.id)
        .first()
    )
    db_credential.name = update_data.name
    db_credential.credentialName = update_data.credentialName
    db_credential.encrypted_data = encrypted_data
    db.commit()
    db.refresh(db_credential)

    return_data = {
        "id": db_credential.id,
        "name": db_credential.name,
        "credentialName": db_credential.credentialName,
        "credentialObj": update_data.credentialObj,
    }

    return return_data
