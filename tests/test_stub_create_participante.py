import pytest

from main_testeable_participante import create_particpante, ParticipanteCreate
from doubles.stub.create_participante_stub import (
    StubDB,
    stub_upload_file_to_s3,
    stub_send_email,
    stub_generate_email,
    StubBackground
)

@pytest.mark.asyncio
async def test_create_participante_with_stubbed_db():
    # Datos de entrada
    participante_data = ParticipanteCreate(
        has_read_convocatoria=True,
        has_read_privacy=True,
        name="Stub User",
        email="stub@example.com",
        age=16,
        school_year=5,
        school_name="Stub High",
        language="ENGLISH",
        level="ADVANCED",
        guardian_name="Parent",
        guardian_email="parent@example.com",
        guardian_phone="1234567890",
        sede_id=99
    )

    # Ejecuto la función bajo prueba usando los stubs
    result = await create_particpante(
        db=StubDB(),
        participante_data=participante_data,
        legal_form_file=object(),
        background_tasks=StubBackground(),
        upload_file_to_s3=stub_upload_file_to_s3,
        send_html_email=stub_send_email,
        participante_registration_email=stub_generate_email
    )

    # Aserciones sobre el resultado
    assert result.email == "stub@example.com"
    assert result.sede_id == 99