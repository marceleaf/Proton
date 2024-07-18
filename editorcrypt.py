import cryptography.fernet as Fernet
import keyring
import uuid

def cryp():
    userId = str(uuid.uuid4())

    serviceId = 'ProtonTE'
    userId = keyring.get_password(serviceId, 'userId')

    if not userId:
        userId = str(uuid.uuid4())
        keyring.set_password(serviceId, 'userId', userId)

        key = Fernet.Fernet.generate_key()
        keyring.set_password(serviceId, userId, key.decode())
    else:
        key = keyring.get_password(serviceId, userId).encode()

    return key