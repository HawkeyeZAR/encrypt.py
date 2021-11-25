import sys
from cryptography.fernet import Fernet


class FileEncryption:
    '''
        Takes three arguments, [in_file] [out_file] [option]
        Contains Two Functions, encrypt_data and decrypt_data
        Usage: python encrypt.py in_file out_file option

        Not recommended for files larger than 1GB
    '''

    def __init__(self):
        key = b'zfc5YzReN3ErLJ54iCesl5lSrE2tGNTVdi3ocxS89CU='
        self.f = Fernet(key)
        self.signature = b'Fernet'

    def encrypt_data(self, in_file, out_file):
        '''
            Takes two inputs:
            in_file: File to be encrypted
            out_file: Save encrypted file as a new file
        '''
        try:
            with open(in_file, "rb") as file:
                data = file.readlines()
                
            #  Encrypt the read data
            encrypted_data = self.f.encrypt(b"".join(data))
            
            try:
                with open(out_file, "wb") as file:
                    #  Add encryption signature to encrypted data
                    file.write(self.signature + encrypted_data)
            except Exception:
                print("There was an error saving the file")
        except FileNotFoundError:
            print(f"Sorry, the file {in_file} does not exist.")
            
    def decrypt_data(self, in_file, out_file):
        '''
            Takes two inputs:
            in_file: File that is encrypted
            out_file: Save uncrypted data to a new file
        '''
        try:
            with open(in_file, "rb") as file:
                data = file.readlines()
            data = b"".join(data)
            
            #  Check if the data has been encrypted
            if self.check_if_encrypted(data):
                try:
                    #  Remove encryption signature from data
                    data = data.replace(self.signature, b"")
                    
                    with open(out_file, "wb") as file:
                        file.write(self.f.decrypt(data))
                except Exception:
                    print("There was an error writing to the file")
        except FileNotFoundError:
            print(f"Sorry, the file {in_file} does not exist.")
            
    def check_if_encrypted(self, data):
        '''
            Takes one input: data
            Checks to see if the data contains encrypted data.

            return True  - If data is encrypted
            
        '''
        if data.startswith(self.signature):
            return True
        else:
            print('Sorry, this file is not encrypted.')


def main(argv):
    '''
        Takes three args, [in_file] [out_file] [option]

        Options are: [encrypt] and [decrypt]

        Check to see if all args are entered and if option chosen is valid
    '''
    if len(argv) != 3:
        print(f"Incorrect usage, {argv}")
        print("Correct Usage: python encrypt.py [in_file] [out_file] [option]")
    else:
        encrypt = FileEncryption()
        
        if argv[2] == 'encrypt':
            encrypt.encrypt_data(argv[0], argv[1])
        elif argv[2] == 'decrypt':
            encrypt.decrypt_data(argv[0], argv[1])
        else:
            print("That option does not exist")
            print("Valid options are: encrypt, decrypt")
    
if __name__ == '__main__':
    main(sys.argv[1:])

