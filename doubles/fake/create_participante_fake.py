# doubles/fake/test_create_particpante_fake.py
import pytest
from main_testeable_participante import create_particpante, ParticipanteCreate, Sede

@pytest.mark.asyncio
async def test_create_participante_with_fake_db():
    class FakeDB:
        def __init__(self):
            self.sedes = {
                1: Sede(id=1, name="CDMX", status="APPROVED")
            }
            self.participantes = []

        def query_sede(self, sede_id):
            return self.sedes.get(sede_id)

        def find_participante_by_email(self, email):
            for p in self.participantes:
                if p.email == email:
                    return p
            return None

        def add(self, obj):
            self.participantes.append(obj)

        def commit(self): pass
        def refresh(self, obj): pass
        def rollback(self): pass

    async def fake_upload_file_to_s3(file, filename, content_type):
        return "fake-legal-key.pdf"

    def fake_send_email(*args, **kwargs): pass

    def fake_generate_email(**kwargs):
        return "<p>Fake Email Body</p>"

    class FakeBackground:
        def add_task(self, fn, *args, **kwargs): pass

    participante_data = ParticipanteCreate(
        has_read_convocatoria=True,
        has_read_privacy=True,
        name="Fake User",
        email="fake@example.com",
        age=17,
        school_year=4,
        school_name="Fake School",
        language="SPANISH",
        level="BASIC",
        guardian_name="Mom",
        guardian_email="mom@example.com",
        guardian_phone="9876543210",
        sede_id=1
    )

    fake_file = object()
    db = FakeDB()

    result = await create_particpante(
        db=db,
        participante_data=participante_data,
        legal_form_file=fake_file,
        background_tasks=FakeBackground(),
        upload_file_to_s3=fake_upload_file_to_s3,
        send_html_email=fake_send_email,
        participante_registration_email=fake_generate_email
    )

    assert result.email == "fake@example.com"
    assert len(db.participantes) == 1
