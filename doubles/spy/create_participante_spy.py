from unittest.mock import AsyncMock, Mock

def get_spy_s3_uploader():
    """
    Un AsyncMock preconfigurado para simular upload_file_to_s3.
    """
    spy = AsyncMock(return_value="spy-legal.pdf")
    return spy

class SpyEmailSender:
    """
    Un Mock callable para simular send_html_email.
    """
    def __init__(self):
        self.send = Mock()

    def __call__(self, *args, **kwargs):
        return self.send(*args, **kwargs)