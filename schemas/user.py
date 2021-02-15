from typing import Optional

from pydantic import BaseModel, EmailStr

#shared properties
class user_base(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    full_name: Optional[str] = None

class user_create(user_base):
    email: EmailStr

 