import pytest
from doubles.dummy.create_participante_dummy import DummyBackgroundTasks,StubDB,fake_upload_file_to_s3,fake_participante_email,dummy_send_email,participante_data,fake_file
from main_testeable_participante import create_particpante, ParticipanteCreate, Sede

@pytest.mark.asyncio
async def test_create_participante_with_dummy_background():
    participante = await create_particpante(
            db=StubDB(),
            participante_data=participante_data,
            legal_form_file=fake_file,
            background_tasks=DummyBackgroundTasks(),
            upload_file_to_s3=fake_upload_file_to_s3,
            send_html_email=dummy_send_email,
            participante_registration_email=fake_participante_email
        )

    assert participante.name == "Test User"