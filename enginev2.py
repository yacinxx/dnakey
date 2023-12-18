from cryptography.fernet import Fernet
import random, json, string, datetime
from profile_config.config_manager import ConfigManager
from license.license_manager import VERSION

class DNAEngine():
    def __init__(
            self, 
            has_key="test", 
            profile_name="profile_test", 
            activate_merge=True, 
            save_cookies=True, 
            **advance_settings):
        
        self.has_key = has_key
        self.profile_name = profile_name
        self.length = advance_settings.get("length", 40)
        self.has_lower = advance_settings.get("has_lower", True)
        self.has_upper = advance_settings.get("has_upper", True)
        self.has_number = advance_settings.get("has_number", True)
        self.has_symbol = advance_settings.get("has_symbol", False)
        self.has_arabic = advance_settings.get("has_arabic", False)
        self.activate_merge = activate_merge
        self.save_cookies = save_cookies
        # Create a Fernet object with the secret key
        secret_key = self.has_key.encode("utf-8")
        self.fernet = Fernet(secret_key)
        self.create_date = datetime.datetime.now()
        # Convert datetime to string
        self.formatted_datetime = self.create_date.isoformat()
        self.random_func = {
            "lower": self.get_random_lower,
            "upper": self.get_random_upper,
            "number": self.get_random_number,
            "symbol": self.get_random_symbol,
            "arabic": self.get_random_arabic
        }
                
    def create_id_profile(self):
        self.config_has_key = f"dnakey${self.has_key[:32:2]}"
        self.config_manager = ConfigManager(self.config_has_key)  
        self.created_profiles = self.config_manager.update_created_profiles()
        self.add_new_profile_cookies()
        self.config_manager.update_config()
        return self.config_has_key, self.created_profiles

    def add_new_profile_cookies(self):
        self.config_manager.update_profile_activity(self.created_profiles, 
                                             self.activate_merge, 
                                             self.save_cookies, 
                                             self.formatted_datetime)

    def generate_password(self):
        types_count = sum([self.has_lower, 
                           self.has_upper, 
                           self.has_number, 
                           self.has_symbol, 
                           self.has_arabic])
        types_arr = [{"lower": self.has_lower}, 
                     {"upper": self.has_upper}, 
                     {"number": self.has_number}, 
                     {"symbol": self.has_symbol}, 
                     {"arabic": self.has_arabic}]
        types_arr = [item for item in types_arr if list(item.values())[0]]
        if types_count == 0:
            return ''
        generated_password = ''
        for _ in range(self.length):
            type_index = random.choice([i for i in range(types_count)])
            func_name = list(types_arr[type_index].keys())[0]
            generated_password += self.random_func[func_name]()
        return generated_password

    def get_random_lower(self):
        return chr(random.randint(97, 122))

    def get_random_upper(self):
        return chr(random.randint(65, 90))

    def get_random_number(self):
        return chr(random.randint(48, 57))

    def get_random_symbol(self):
        symbol_ranges = [
            (33, 47),  # ASCII values for common symbols
            (58, 64),
            (91, 96),
            (123, 126)
        ]
        random_range = random.choice(symbol_ranges)
        return chr(random.randint(random_range[0], random_range[1]))

    def get_random_arabic(self):
        arabic_list = ['ا','ب','ج','د','ه','و','ز','ح','ط','ي','ك','ل','م','ن','س','ع','ف','ص','ق','ر','ش','ت','ث','خ','ذ','ض','ظ','غ']
        return random.choice(list(arabic_list))

    def generate_dnakey_profile(self):
        dna_token = [None] * 36
        for i in range(len(dna_token)):
            dna_token[i] = self.generate_password()
        dna_brain = {
            "A": [{"upper": dna_token[0]}],
            "B": [{"upper": dna_token[1]}],
            "C": [{"upper": dna_token[2]}],
            "D": [{"upper": dna_token[3]}],
            "E": [{"upper": dna_token[4]}],
            "F": [{"upper": dna_token[5]}],
            "G": [{"upper": dna_token[6]}],
            "H": [{"upper": dna_token[7]}],
            "I": [{"upper": dna_token[8]}],
            "J": [{"upper": dna_token[9]}],
            "K": [{"upper": dna_token[10]}],
            "L": [{"upper": dna_token[11]}],
            "M": [{"upper": dna_token[12]}],
            "N": [{"upper": dna_token[13]}],
            "O": [{"upper": dna_token[14]}],
            "P": [{"upper": dna_token[15]}],
            "Q": [{"upper": dna_token[16]}],
            "R": [{"upper": dna_token[17]}],
            "S": [{"upper": dna_token[18]}],
            "T": [{"upper": dna_token[19]}],
            "U": [{"upper": dna_token[20]}],
            "V": [{"upper": dna_token[21]}],
            "W": [{"upper": dna_token[22]}],
            "X": [{"upper": dna_token[23]}],
            "Y": [{"upper": dna_token[24]}],
            "Z": [{"upper": dna_token[25]}],
            "0": [{"number": dna_token[26]}],
            "1": [{"number": dna_token[27]}],
            "2": [{"number": dna_token[28]}],
            "3": [{"number": dna_token[29]}],
            "4": [{"number": dna_token[30]}],
            "5": [{"number": dna_token[31]}],
            "6": [{"number": dna_token[32]}],
            "7": [{"number": dna_token[33]}],
            "8": [{"number": dna_token[34]}],
            "9": [{"number": dna_token[35]}]    
            }

        # Loading the lowercase alphabet to a list
        self.alphabet = list(string.ascii_uppercase)
        for letter in self.alphabet:
            self.upper_sequence = dna_brain[letter][0]
            self.lower_list = [self.upper_sequence["upper"][i:i + 4] for i in range(0, len(self.upper_sequence["upper"]), 4)]
            high_len = self.length // 4
            lower_len = high_len // 2
            self.block = self.lower_list[lower_len : high_len] + self.lower_list[:lower_len]
            self.lower = ''.join(self.block)
            self.upper_sequence.update({"lower": self.lower})
        return dna_brain

    def create_dnakey_profile(self):
        prime_id, profile_id = self.create_id_profile()
        meta_data = {
            "prime_id": prime_id, 
            "profile_id": profile_id, 
            "profile_name": self.profile_name, 
            "profile_length": self.length, 
            "activate_merge": self.activate_merge, 
            "save_cookies": self.save_cookies, 
            "date_time": self.formatted_datetime, 
            "version": VERSION, 
            "request_status": "online"
            }    
        dna_brain = {
            "meta_data": meta_data, 
            "profile_brain": self.generate_dnakey_profile()
            }
        json_string = json.dumps(dna_brain, indent=3)
        # Encrypt the JSON data string
        encrypted_data = self.fernet.encrypt(json_string.encode())
        return encrypted_data, dna_brain