# tests/test_mock_create_participante.py

import pytest
from main_testeable_participante import create_particpante
from doubles.mock.create_participante_mock import (
    MockDB,
    MockBackground,
    participante_data,
    upload_mock,
    email_mock,
    email_builder_mock
)

@pytest.mark.asyncio
async def test_create_participante_with_full_mock():
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
    email_mock.assert_called_once_with(
        ["mocky@example.com"],
        "Registro recibido",
        "<p>Mocked email</p>"
    )

    assert db.last_added.email == "mocky@example.com"
    assert result.name == "Mocky"