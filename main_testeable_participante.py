# main_testable_participante.py
from typing import List, Literal
from pydantic import BaseModel, EmailStr

class ParticipanteCreate(BaseModel):
    has_read_convocatoria: bool
    has_read_privacy: bool

    name: str
    email: EmailStr
    age: int
    school_year: int
    school_name: str

    language: Literal["SPANISH", "ENGLISH"]
    level: Literal["ADVANCED", "BASIC"]

    guardian_name: str
    guardian_email: str
    guardian_phone: str

    sede_id: int

class Sede:
    def __init__(self, id, name, status):
        self.id = id
        self.name = name
        self.status = status

class Participante:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

# The function under test (testable version of create_particpante)
async def create_particpante(
    db, 
    participante_data: ParticipanteCreate, 
    legal_form_file,  # file-like object
    background_tasks,
    upload_file_to_s3,
    send_html_email,
    participante_registration_email
):
    sede = db.query_sede(participante_data.sede_id)
    if not sede:
        raise Exception("Sede not found")
    if sede.status != "APPROVED":
        raise Exception("Sede not approved")

    existing = db.find_participante_by_email(participante_data.email)
    if existing:
        raise Exception("Participante already exists")

    if not participante_data.has_read_convocatoria or not participante_data.has_read_privacy:
        raise Exception("Terms not accepted")

    try:
        legal_form_key = await upload_file_to_s3(
            legal_form_file,
            "legal.pdf",
            content_type="application/pdf"
        )
    except Exception as e:
        raise Exception(f"Upload failed: {str(e)}")

    new_participante = Participante(
        has_read_convocatoria=participante_data.has_read_convocatoria,
        has_read_privacy=participante_data.has_read_privacy,
        legal_form_key=legal_form_key,
        name=participante_data.name,
        age=participante_data.age,
        email=participante_data.email,
        school_year=participante_data.school_year,
        school_name=participante_data.school_name,
        language=participante_data.language,
        level=participante_data.level,
        guardian_phone=participante_data.guardian_phone,
        guardian_name=participante_data.guardian_name,
        guardian_email=participante_data.guardian_email,
        status="PENDING",
        sede_id=participante_data.sede_id,
    )

    try:
        db.add(new_participante)
        db.commit()
        db.refresh(new_participante)

        email_body = participante_registration_email(
            name=new_participante.name,
            sede_name=sede.name,
            level=new_participante.level,
            language=new_participante.language,
        )
        background_tasks.add_task(send_html_email, [new_participante.email], "Registro recibido", email_body)

        return new_participante
    except Exception as e:
        db.rollback()
        raise Exception("DB error") from e
