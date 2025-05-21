# doubles/spy/test_create_particpante_spy.py
import pytest
from unittest.mock import Mock
from main_testeable_participante import create_particpante, ParticipanteCreate, Sede
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_create_participante_with_spy_on_services():
    class SimpleDB:
        def query_sede(self, sede_id):
            return Sede(id=1, name="CDMX", status="APPROVED")

        def find_participante_by_email(self, email):
            return None

        def add(self, obj): pass
        def commit(self): pass
        def refresh(self, obj): pass
        def rollback(self): pass

    spy_upload = AsyncMock(return_value="spy-legal.pdf")

    spy_upload.return_value = "spy-legal.pdf"

    spy_send_email = Mock()

    def dummy_generate_email(**kwargs):
        return "<p>Generated Spy Email</p>"

    class Background:
        def add_task(self, fn, *args, **kwargs):
            fn(*args, **kwargs)

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

    result = await create_particpante(
        db=SimpleDB(),
        participante_data=participante_data,
        legal_form_file=object(),
        background_tasks=Background(),
        upload_file_to_s3=spy_upload,
        send_html_email=spy_send_email,
        participante_registration_email=dummy_generate_email
    )

    spy_upload.assert_called_once()
    spy_send_email.assert_called_once()
    assert result.name == "Spy Tester"
