import pytest
import os
from src.hw3 import task2_requests as t


@pytest.mark.asyncio
async def test_images_are_downloaded(tmp_path):
    await t.download_images(tmp_path, 2)
    assert len([1 for x in list(os.scandir(tmp_path)) if x.is_file()]) == 2
