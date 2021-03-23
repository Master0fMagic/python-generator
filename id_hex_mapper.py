

class IdHexMapper:
    @staticmethod
    def id_to_hex_string(id:int) -> str:
        hex_id = hex(id)
        return ('0'*(10-len(hex_id)) + hex_id).upper()[2:]
    
    @staticmethod
    def hex_id_to_int(id:str) -> int:
        return int('0x'+id, 16)   