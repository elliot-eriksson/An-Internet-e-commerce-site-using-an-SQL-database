import bcrypt 


def encrypPassword(password):
    
    # converting password to array of bytes 
    bytes = password.encode('utf-8') 
    
    # generating the salt 
    salt = bcrypt.gensalt()
    
    # Hashing the password 
    hash = bcrypt.hashpw(bytes, salt) 

    return hash
    

def decryptPassword(password, currentPass):
    userBytes = password.encode('utf-8') 
    
    # checking password 
    result = bcrypt.checkpw(userBytes, currentPass) 
    return result
