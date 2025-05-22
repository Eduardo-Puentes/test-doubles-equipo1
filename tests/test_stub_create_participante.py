import pytest
from main_testeable_participante import create_particpante, ParticipanteCreate
from doubles.stub.create_participante_stub import (
    StubDB,
    stub_upload_file_to_s3,
    stub_send_email,
    stub_generate_email,
    StubBackground
)

@pytest.mark.asyncio
async def test_stub_returns_correct_email_and_sede():
    data = ParticipanteCreate(
        has_read_convocatoria=True, has_read_privacy=True,
        name="Stub User", email="stub@example.com",
        age=16, school_year=5, school_name="Stub High",
        language="ENGLISH", level="ADVANCED",
        guardian_name="P", guardian_email="p@e", guardian_phone="111",
        sede_id=99
    )
    res = await create_particpante(
        db=StubDB(), participante_data=data,
        legal_form_file=object(), background_tasks=StubBackground(),
        upload_file_to_s3=stub_upload_file_to_s3,
        send_html_email=stub_send_email,
        participante_registration_email=stub_generate_email
    )
    assert res.email == "stub@example.com"
    assert res.sede_id == 99

@pytest.mark.asyncio
async def test_stub_upload_returns_key():
    key = await stub_upload_file_to_s3("f","n","t")
    assert key == "legal-key.pdf"

def test_stub_send_email_noop():
    stub_send_email("a@b","S","B")

def test_stub_generate_email_contains_tag():
    html = stub_generate_email(name="X")
    assert "<p>" in html

def test_stub_background_multiple_calls():
    bg = StubBackground()
    for _ in range(4):
        bg.add_task(lambda: None)