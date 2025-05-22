import pytest
from doubles.dummy.create_participante_dummy import (
    DummyBackgroundTasks,
    StubDB,
    fake_upload_file_to_s3,
    fake_participante_email,
    dummy_send_email,
    participante_data,
    fake_file
)
from main_testeable_participante import create_particpante

@pytest.mark.asyncio
async def test_dummy_background_tasks_runs_without_error():
    result = await create_particpante(
        db=StubDB(),
        participante_data=participante_data,
        legal_form_file=fake_file,
        background_tasks=DummyBackgroundTasks(),
        upload_file_to_s3=fake_upload_file_to_s3,
        send_html_email=dummy_send_email,
        participante_registration_email=fake_participante_email
    )
    assert result.name == "Test User"

@pytest.mark.asyncio
async def test_dummy_upload_returns_fixed_key():
    key = await fake_upload_file_to_s3("file", "name", "type")
    assert key == "file-key.pdf"

def test_dummy_email_generator_returns_html():
    html = fake_participante_email(name="X")
    assert html.startswith("<p>") and html.endswith("</p>")

def test_dummy_send_email_is_noop():
    dummy_send_email("a@b.com", "S", "<p>hi</p>")

def test_dummy_background_multiple_calls():
    tasks = DummyBackgroundTasks()
    for _ in range(3):
        tasks.add_task(lambda: None)