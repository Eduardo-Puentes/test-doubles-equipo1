# tests/test_fake_create_participante.py

import pytest
from doubles.fake.create_participante_fake import (
    FakeDB, FakeBackground,
    fake_upload_file_to_s3,
    fake_send_email,
    fake_generate_email
)
from main_testeable_participante import create_particpante, ParticipanteCreate

@pytest.mark.asyncio
async def test_create_participante_with_fake_db():
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