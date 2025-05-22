import pytest
from doubles.fake.create_participante_fake import (
    FakeDB, FakeBackground,
    fake_upload_file_to_s3,
    fake_send_email,
    fake_generate_email
)
from main_testeable_participante import create_particpante, ParticipanteCreate

@pytest.mark.asyncio
async def test_fake_db_inserts_one_participant():
    db = FakeDB()
    data = ParticipanteCreate(
        has_read_convocatoria=True, has_read_privacy=True,
        name="Fake User", email="fake@example.com",
        age=17, school_year=4, school_name="Fake School",
        language="SPANISH", level="BASIC",
        guardian_name="Mom", guardian_email="mom@example.com", guardian_phone="9876543210",
        sede_id=1
    )
    res = await create_particpante(
        db=db, participante_data=data,
        legal_form_file=object(),
        background_tasks=FakeBackground(),
        upload_file_to_s3=fake_upload_file_to_s3,
        send_html_email=fake_send_email,
        participante_registration_email=fake_generate_email
    )
    assert res.email == "fake@example.com"
    assert len(db.participantes) == 1

@pytest.mark.asyncio
async def test_fake_upload_and_commit_called():
    db = FakeDB()
    await fake_upload_file_to_s3("f","n","t")

def test_fake_send_email_records_call(monkeypatch):
    called = {}
    def fake_send(to, subject, body):
        called['ok'] = True
    fake_send_email("x@y.com", "Hi", "Body")

def test_fake_generate_email_content():
    html = fake_generate_email(name="Z")
    assert html == "<p>Fake Email Body</p>"

def test_fake_background_noop_multiple():
    bg = FakeBackground()
    for _ in range(3):
        bg.add_task(lambda: None)