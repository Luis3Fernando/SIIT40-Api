from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import LoginDTO
from app.core.security import SecurityUtils

class AuthService:
    def login(self, db: Session, credentials: LoginDTO):
        """Valida credenciales y entrega los tokens"""
        user = db.query(User).filter(User.email == credentials.email).first()
        
        if not user:
            return {"error": "El correo electrónico no se encuentra registrado"}
            
        if not SecurityUtils.verify_password(credentials.password, user.password):
            return {"error": "La contraseña ingresada es incorrecta"}
            
        tokens = SecurityUtils.generate_token_pair(user.id)
        
        return {
            "id": user.id,
            "fullName": user.full_name,
            "email": user.email,
            **tokens
        }

    def refresh_token(self, token_data: str):
        """Verifica el refresh token y otorga un nuevo access token"""
        payload = SecurityUtils.decode_token(token_data)
        
        if "error" in payload:
            return {"error": payload["error"]}
            
        if payload.get("type") != "refresh":
            return {"error": "Token no válido para esta operación"}
            
        user_id = payload.get("sub")
        return SecurityUtils.generate_token_pair(int(user_id))

auth_service = AuthService()