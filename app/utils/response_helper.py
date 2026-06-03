from typing import Any, List
from app.schemas.base_response import APIResponse, MessageDTO

class ResponseHelper:
    
    @staticmethod
    def success(message: str, data: Any = None, msg_type: str = "success") -> dict:
        """Retorna una estructura estandarizada de éxito"""
        return {
            "status": "success",
            "message": [
                {
                    "type": msg_type,
                    "message": message
                }
            ],
            "data": data
        }

    @staticmethod
    def error(message: str, msg_type: str = "error", data: Any = None) -> dict:
        """Retorna una estructura estandarizada de error"""
        return {
            "status": "error",
            "message": [
                {
                    "type": msg_type,
                    "message": message
                }
            ],
            "data": data
        }