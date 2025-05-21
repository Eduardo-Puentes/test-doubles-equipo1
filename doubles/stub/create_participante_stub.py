from main_testeable_participante import Sede

class StubDB:
    """
    Simula la base de datos para create_participante:
    - query_sede devuelve siempre una Sede ficticia.
    - find_participante_by_email siempre None (usuario nuevo).
    """
    def query_sede(self, sede_id):
        return Sede(id=99, name="Querétaro", status="APPROVED")

    def find_participante_by_email(self, email):
        return None

    def add(self, obj):
        pass

    def commit(self):
        pass

    def refresh(self, obj):
        pass

async def stub_upload_file_to_s3(file, filename, content_type):
    """Async stub que simula subida a S3."""
    return "legal-key.pdf"

def stub_send_email(*args, **kwargs):
    """Stub que simula el envío de correo sin hacer nada."""
    pass

def stub_generate_email(**kwargs):
    """Stub que genera un HTML de mail genérico."""
    return "<p>Welcome Email</p>"

class StubBackground:
    """Stub de background_tasks que ignora las tareas."""
    def add_task(self, fn, *args, **kwargs):
        pass