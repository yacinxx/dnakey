from streamlit import toast, info, error
from profile_config.config_manager import ConfigManager
import time

class PrimeKeyConfig:
    def agent_prime_key(self, hash_key:str) -> str | int:
        MAX_LENGTH = 56
        self.hash_key = hash_key
        if (self.hash_key) and (len(self.hash_key) == MAX_LENGTH) and (self.hash_key.startswith("dnakey$")):
            positions_to_remove = [10, 20, 30, 40, 48]
            self.hash_key = self.hash_key.replace('dnakey$', '')
            is_prime = ''.join([self.hash_key[i] for i in positions_to_remove])
            if is_prime == "PRIME":
                valid_hash_key = ''.join([self.hash_key[i] for i in range(len(self.hash_key)) if i not in positions_to_remove])
                config_has_key = f"dnakey${valid_hash_key[:32:2]}"
                config_manager = list(ConfigManager(config_has_key).configuration().keys())
                if config_has_key in config_manager:
                    toast("**:blue[The Prime key is valid!]**", icon="🧁")
                    time.sleep(1)
                    return valid_hash_key
                else:
                    info("This Prime key not registered yet!", icon="😮")
                    return 1                    
            else:
                error("This is not a Prime key!")
                return 1
        elif self.hash_key and len(self.hash_key) != MAX_LENGTH:
            error("The Prime key is not valid!")
            return 1
        else:
            return 1