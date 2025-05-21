# doubles/fake/create_participante_fake.py

from main_testeable_participante import create_particpante, ParticipanteCreate, Sede

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