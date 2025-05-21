# doubles/mock/test_create_particpante_mock.py
import pytest
from unittest.mock import Mock
from main_testeable_participante import create_particpante, ParticipanteCreate, Sede
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_create_participante_with_full_mock():
    class MockDB:
        def query_sede(self, sede_id):
            return Sede(id=1, name="Mock City", status="APPROVED")

        def find_participante_by_email(self, email): return None
        def add(self, obj): self.last_added = obj
        def commit(self): self.committed = True
        def refresh(self, obj): pass
        def rollback(self): self.rolled_back = True

    upload_mock = AsyncMock(return_value="mocked-legal-form.pdf")
    email_mock = Mock()
    email_builder_mock = Mock(return_value="<p>Mocked email</p>")

    class MockBackground:
        def __init__(self):
            self.tasks = []
        def add_task(self, fn, *args, **kwargs):
            self.tasks.append((fn, args, kwargs))
            fn(*args, **kwargs)

    participante_data = ParticipanteCreate(
        has_read_convocatoria=True,
        has_read_privacy=True,
        name="Mocky",
        email="mocky@example.com",
        age=20,
        school_year=6,
        school_name="Mock School",
        language="SPANISH",
        level="BASIC",
        guardian_name="Mom",
        guardian_email="mom@mock.com",
        guardian_phone="000111222",
        sede_id=1
    )

    db = MockDB()
    bg = MockBackground()

    result = await create_particpante(
        db=db,
        participante_data=participante_data,
        legal_form_file=object(),
        background_tasks=bg,
        upload_file_to_s3=upload_mock,
        send_html_email=email_mock,
        participante_registration_email=email_builder_mock
    )

    upload_mock.assert_called_once()
    email_builder_mock.assert_called_once()
    email_mock.assert_called_once_with([
        "mocky@example.com"], "Registro recibido", "<p>Mocked email</p>")

    assert db.last_added.email == "mocky@example.com"
    assert result.name == "Mocky"
