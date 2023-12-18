import string

class Merge:
    def __init__(self, profile_1:dict, profile_2:dict) -> None:
        self.profile_1 = profile_1
        self.profile_2 = profile_2
        self.alphabet = list(string.ascii_uppercase)
        self.numbers = [i.__str__() for i in string.digits]
        self.profile_name = self.profile_1.get("meta_data", {}).get("profile_name", None)
        self.length = self.profile_1.get("meta_data", {}).get("profile_length", None)
        self.profile_id = self.profile_1.get("meta_data", {}).get("profile_id", None)
        self.merge_with = self.profile_2.get("meta_data", {}).get("profile_id", None)

    def get_merge_error(self):
        if self.length != self.profile_2.get("meta_data", {}).get("profile_length", None):
            return 1

    def empty_brain(self):
        return {
            "meta_data": {
            "profile_name": self.profile_name,
            "profile_id": self.profile_id,
            "merge_with": self.merge_with,
            "profile_length": self.length,
            "action_status": "merge profiles"
            },
            "profile_brain": {
                "A": [{}],
                "B": [{}],
                "C": [{}],
                "D": [{}],
                "E": [{}],
                "F": [{}],
                "G": [{}],
                "H": [{}],
                "I": [{}],
                "J": [{}],
                "K": [{}],
                "L": [{}],
                "M": [{}],
                "N": [{}],
                "O": [{}],
                "P": [{}],
                "Q": [{}],
                "R": [{}],
                "S": [{}],
                "T": [{}],
                "U": [{}],
                "V": [{}],
                "W": [{}],
                "X": [{}],
                "Y": [{}],
                "Z": [{}],
                "0": [{}],
                "1": [{}],
                "2": [{}],
                "3": [{}],
                "4": [{}],
                "5": [{}],
                "6": [{}],
                "7": [{}],
                "8": [{}],
                "9": [{}]
            }
        }
        
    def merge_brain(self):
        self.dna_brain_merge = self.empty_brain()
        self.dna_brain_length = self.length // 2
        for num, letter in enumerate(self.alphabet):
            letter_sequence = self.dna_brain_merge["profile_brain"][letter][0]
            p_1 = self.profile_1["profile_brain"][letter][0]
            p_2 = self.profile_2["profile_brain"][letter][0]
            upper = p_2["upper"][self.dna_brain_length:] + p_1["upper"][:self.dna_brain_length]
            lower = p_2["lower"][self.dna_brain_length:] + p_1["lower"][:self.dna_brain_length]
            letter_sequence.update({"upper": upper, "lower": lower})
            if num < 10:
                number = self.numbers[num]
                number_sequence = self.dna_brain_merge["profile_brain"][number][0]
                p_1 = self.profile_1["profile_brain"][number][0]
                p_2 = self.profile_2["profile_brain"][number][0]
                number = p_2["number"][self.dna_brain_length:] + p_1["number"][:self.dna_brain_length]
                number_sequence.update({"number": number})
        return self.dna_brain_merge