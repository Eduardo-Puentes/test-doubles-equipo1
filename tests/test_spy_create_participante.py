import pytest

from main_testeable_participante import (
    create_particpante,
    ParticipanteCreate,
    Sede
)
from doubles.spy.create_participante_spy import get_spy_s3_uploader, SpyEmailSender

# Un DB simplificado solo para el test
class SimpleDB:
    def query_sede(self, sede_id):
        return Sede(id=1, name="CDMX", status="APPROVED")

    def find_participante_by_email(self, email):
        return None

    def add(self, obj): pass
    def commit(self): pass
    def refresh(self, obj): pass
    def rollback(self): pass

# Un background_tasks que ejecuta al vuelo
class Background:
    def add_task(self, fn, *args, **kwargs):
        fn(*args, **kwargs)

@pytest.mark.asyncio
async def test_create_participante_with_spy_on_services():
    # — Configuro los Spies —
    spy_upload = get_spy_s3_uploader()
    spy_email = SpyEmailSender()

    # Datos de entrada
    participante_data = ParticipanteCreate(
        has_read_convocatoria=True,
        has_read_privacy=True,
        name="Spy Tester",
        email="spy@example.com",
        age=18,
        school_year=3,
        school_name="Spy School",
        language="ENGLISH",
        level="ADVANCED",
        guardian_name="Guardian",
        guardian_email="guardian@spy.com",
        guardian_phone="1122334455",
        sede_id=1
    )

    # — Ejecuto la función bajo prueba —
    result = await create_particpante(
        db=SimpleDB(),
        participante_data=participante_data,
        legal_form_file=object(),
        background_tasks=Background(),
        upload_file_to_s3=spy_upload,
        send_html_email=spy_email,
        participante_registration_email=lambda **kwargs: "<p>Generated Spy Email</p>"
    )

    # — Aserciones sobre los Spies —
    spy_upload.assert_awaited_once()
    spy_email.send.assert_called_once()
    assert result.name == "Spy Tester"