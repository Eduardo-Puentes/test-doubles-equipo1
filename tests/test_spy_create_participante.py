import pytest
from main_testeable_participante import (
    create_particpante,
    ParticipanteCreate,
    Sede
)
from doubles.spy.create_participante_spy import get_spy_s3_uploader, SpyEmailSender

class SimpleDB:
    def query_sede(self, sede_id):
        return Sede(id=1, name="CDMX", status="APPROVED")
    def find_participante_by_email(self, email): return None
    def add(self, obj): pass
    def commit(self): pass
    def refresh(self, obj): pass
    def rollback(self): pass

class Background:
    def add_task(self, fn, *args, **kwargs):
        fn(*args, **kwargs)

@pytest.mark.asyncio
async def test_spy_records_upload_and_email_and_name():
    spy_upload = get_spy_s3_uploader()
    spy_email = SpyEmailSender()
    data = ParticipanteCreate(
        has_read_convocatoria=True, has_read_privacy=True,
        name="Spy Tester", email="spy@example.com",
        age=18, school_year=3, school_name="Spy School",
        language="ENGLISH", level="ADVANCED",
        guardian_name="G", guardian_email="g@e.com", guardian_phone="111",
        sede_id=1
    )
    res = await create_particpante(
        db=SimpleDB(), participante_data=data,
        legal_form_file=object(), background_tasks=Background(),
        upload_file_to_s3=spy_upload,
        send_html_email=spy_email,
        participante_registration_email=lambda **kw: "<p>Hi</p>"
    )
    spy_upload.assert_awaited_once()
    spy_email.send.assert_called_once()
    assert res.name == "Spy Tester"

@pytest.mark.asyncio
async def test_spy_multiple_upload_calls():
    spy = get_spy_s3_uploader()
    await spy("a","b","c")
    spy.assert_awaited_once()

def test_spy_email_send_no_args():
    spy = SpyEmailSender()
    spy.send("x@y", "S", "B")
    assert spy.send.call_count == 1

def test_spy_background_noop_multiple():
    bg = Background()
    for _ in range(4):
        bg.add_task(lambda: None)