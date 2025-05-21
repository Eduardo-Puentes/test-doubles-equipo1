# doubles/mock/create_participante_mock.py

from unittest.mock import Mock, AsyncMock
from main_testeable_participante import ParticipanteCreate, Sede

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
