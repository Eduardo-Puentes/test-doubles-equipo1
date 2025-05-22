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
async def test_mock_calls_upload_and_email_builder_and_sender():
    db = MockDB()
    bg = MockBackground()
    res = await create_particpante(
        db=db, participante_data=participante_data,
        legal_form_file=object(),
        background_tasks=bg,
        upload_file_to_s3=upload_mock,
        send_html_email=email_mock,
        participante_registration_email=email_builder_mock
    )
    upload_mock.assert_called_once()
    email_builder_mock.assert_called_once()
    email_mock.assert_called_once_with(
        ["mocky@example.com"], "Registro recibido", "<p>Mocked email</p>"
    )
    assert res.name == "Mocky"
    assert db.last_added.email == "mocky@example.com"

@pytest.mark.asyncio
async def test_mock_multiple_upload_calls_reset(monkeypatch):
    upload_mock.reset_mock()
    await upload_mock("a","b","c")
    assert upload_mock.call_count == 1

def test_mock_email_builder_return(monkeypatch):
    html = email_builder_mock(name="X")
    assert "<p>" in html

def test_mock_background_tasks_noop():
    bg = MockBackground()
    for _ in range(4):
        bg.add_task(lambda: None)