# doubles/stub/test_create_particpante_stub.py
import pytest
from main_testeable_participante import create_particpante, ParticipanteCreate, Sede

@pytest.mark.asyncio
async def test_create_participante_with_stubbed_db():
    class StubDB:
        def query_sede(self, sede_id):
            return Sede(id=99, name="Querétaro", status="APPROVED")

        def find_participante_by_email(self, email):
            return None  # Always returns no existing user

        def add(self, obj): pass
        def commit(self): pass
        def refresh(self, obj): pass

    async def stub_upload_file_to_s3(file, filename, content_type):
        return "legal-key.pdf"

    def stub_send_email(*args, **kwargs): pass

    def stub_generate_email(**kwargs):
        return "<p>Welcome Email</p>"

    class StubBackground:
        def add_task(self, fn, *args, **kwargs): pass

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

    stub_file = object()

    result = await create_particpante(
        db=StubDB(),
        participante_data=participante_data,
        legal_form_file=stub_file,
        background_tasks=StubBackground(),
        upload_file_to_s3=stub_upload_file_to_s3,
        send_html_email=stub_send_email,
        participante_registration_email=stub_generate_email
    )

    assert result.email == "stub@example.com"
    assert result.sede_id == 99
