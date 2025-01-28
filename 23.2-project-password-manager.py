from abc import ABC, abstractmethod
from typing import List, Dict

class Credential(ABC):
    def __init__(self, service: str):
        self._service = ""
        
        self._service = service
        
    @property
    def service(self):
        return self._service
    
    @service.setter
    def service(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Service should be a string")
        if value.strip() == "":
            raise ValueError("Can't be an empty string")
        
        self._service = value
        
    @abstractmethod
    def reveal_secret_properties(self) -> Dict:
        pass
    
    @abstractmethod
    def print_credential(self) -> str:
        pass
        
class UsernameAndPassword(Credential):
    def __init__(self, service: str, username: str, password: str):
        super().__init__(service)
        self._username = ""
        self._password = ""
        
        self.username = username
        self.password = password
        
    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Username should be a string")
        if value.strip() == "":
            raise ValueError("Can't be an empty string")
        
        self._username = value
        
    @property
    def password(self):
        return "******"
    
    @password.setter
    def password(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Password should be a string")
        
        stripped_value = value.strip()
        if stripped_value == "":
            raise ValueError("Can't be an empty string")
        if len(stripped_value) < 8:
            raise ValueError("Must be at least 8 characters")
        if any(char.isupper() for char in stripped_value):
            raise ValueError("Must contain at least one uppercase character")
        if any(char.isdigit() for char in stripped_value):
            raise ValueError("Must contain at least one number")
        if all(char.isalnum() for char in stripped_value):
            raise ValueError("Must contain at least one special character")
        
        self._password = stripped_value
        
    def reveal_secret_properties(self):
        return {
            "password": self._password
        }
        
    def print_credential(self) -> str:
        return f"{self.service} --- Username: {self.username}, Password: ******"
        
class CredentialRepository:
    def __init__(self) -> None:
        self._credentials: List[Credential] = []
        
    @property
    def credentials(self):
        return self._credentials
        
    def add_credential(self, credential: Credential):
        if not isinstance(credential, Credential):
            raise TypeError("Pass Credential")
        if credential in self._credentials:
            raise ValueError("This Credential already exists")
        
        self._credentials.append(credential)
        
    def remove_credential(self, credential: Credential):
        if not isinstance(credential, Credential):
            raise TypeError("Pass Credential")
        if credential not in self._credentials:
            raise ValueError("This Credential doesn't exists")
        
        self._credentials.remove(credential)
        
    def update_credential(self, old_credential: Credential, new_credential: Credential):
        if not isinstance(old_credential, Credential) or not isinstance(new_credential, Credential):
            raise TypeError("Pass Credential")
        if new_credential in self._credentials:
            raise ValueError("This Credential already exists")
        if old_credential not in self._credentials:
            raise ValueError("This Credential doesn't exists")
        
        self._credentials.remove(old_credential)
        self._credentials.append(new_credential)
        
    def search_credentials(self, service: str) -> List[Credential]:
        if not isinstance(service, str):
            raise TypeError("Service should be a string")
        if service.strip() == "":
            raise ValueError("Can't be an empty string")
        
        return [credential for credential in self._credentials if credential.service == service]
    
class CredentialUI:
    def __init__(self, repository: CredentialRepository):
        self._repository: CredentialRepository | None = None
        
        self.repository = repository
        
    @property
    def repository(self):
        return self._repository
    
    @repository.setter
    def repository(self, value: CredentialRepository):
        if not isinstance(value, CredentialRepository):
            raise TypeError("Pass a CredentialRepository")
        
        self._repository = value
    
    def select_from_found_credentials(self) -> Credential:
        if not self._repository:
            raise ValueError("Repository not initialized")
            
        while True:
            service = input("From which service do you want to remove a credential? ")
            found_credentials = self._repository.search_credentials(service)
            
            if found_credentials:
                break
        
        if len(found_credentials) > 1:
            print("Found credentials:")
            for index, credential in enumerate(found_credentials):
                print(f"{index}) {credential.print_credential()}")
                
            credential_index = input("Which credential do you want to remove? ")
            while int(credential_index) not in range(0, len(credential_index)):
                credential_index = input("Please select one of the shown above credentials ")
            
            selected_credential = found_credentials[int(credential_index)]
        else:
            selected_credential = found_credentials[0]
            
        return selected_credential
    
    def launch(self):
        while True:
            print("1. View all credentials")
            print("2. Add new credential")
            print("3. Remove existing credential")
            print("4. Reveal hidden properties")
            print(" ")
            print("0. Exit")
            
            action = input("Select an action (0 to 4) ")
            while action not in ("0", "1", "2", "3", "4"):
                action = input("Select a valid action please")
                
            if action == "0":
                break
            
            if action == "1":
                for credential in self._repository:
                    print(credential.print_credential())
                    
            # Currently it only supports username and password
            if action == "2":
                while True:
                    service = input("What is the service? ")
                    username = input("What is the username? ")
                    password = input("What is the password? ")
                    
                    try:
                        credential = UsernameAndPassword(service, username, password)
                    except Exception as error:
                        print(f"Something went wrong: {error}")
                        continue
                    
                    try:
                        self._repository.add_credential(credential)
                    except Exception as error:
                        print(f"Something went wrong: {error}")
                        continue
                    
                    print("Credential successfully added")
                    break
                
            if action == "3":
                while True:
                    selected_credential = self.select_from_found_credentials()
                    
                    try:
                        self._repository.remove_credential(selected_credential)
                    except Exception as error:
                        print(f"An error occurred: {error}")
                        continue
                        
                    print("Credential successfully deleted")    
                    break
            
            if action == "4":
                selected_credential = self.select_from_found_credentials()
                print(selected_credential.reveal_secret_properties())
                    