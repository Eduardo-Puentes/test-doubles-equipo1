# doubles/dummy/test_create_particpante_dummy.py
import pytest
import asyncio
from main_testeable_participante import create_particpante, ParticipanteCreate, Sede

class DummyBackgroundTasks:
    def add_task(self, fn, *args, **kwargs):
        pass  # Not actually used in this test

@pytest.mark.asyncio
async def test_create_participante_with_dummy_background():
    class StubDB:
        def query_sede(self, sede_id):
            return Sede(id=1, name="Puebla", status="APPROVED")

        def find_participante_by_email(self, email):
            return None

        def add(self, obj): pass
        def commit(self): pass
        def refresh(self, obj): pass

    async def fake_upload_file_to_s3(file, filename, content_type):
        return "file-key.pdf"

    def fake_participante_email(**kwargs):
        return "<p>Email body</p>"

    def dummy_send_email(*args, **kwargs): pass

    participante_data = ParticipanteCreate(
        has_read_convocatoria=True,
        has_read_privacy=True,
        name="Test User",
        email="test@example.com",
        age=18,
        school_year=6,
        school_name="Test School",
        language="SPANISH",
        level="BASIC",
        guardian_name="Guardian",
        guardian_email="guardian@example.com",
        guardian_phone="1234567890",
        sede_id=1
    )

    fake_file = object()  # file-like dummy

    participante = await create_particpante(
        db=StubDB(),
        participante_data=participante_data,
        legal_form_file=fake_file,
        background_tasks=DummyBackgroundTasks(),
        upload_file_to_s3=fake_upload_file_to_s3,
        send_html_email=dummy_send_email,
        participante_registration_email=fake_participante_email
    )

    assert participante.name == "Test User"
