import aiohttp
import asyncio
import aiofiles
import os
import argparse
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup


url: str = "https://www.thisfuckeduphomerdoesnotexist.com"


def find_img_url_from_html(html_page: str) -> str:
    """
    :param html_page: html page of 'https://www.thisfuckeduphomerdoesnotexist.com'
    :return: image url
    """
    soup: BeautifulSoup = BeautifulSoup(html_page, "html.parser")
    img_tags: BeautifulSoup.ResultSet = soup.find_all("img", attrs={"class": "image-payload"})
    try:
        return img_tags[0]["src"]
    except (IndexError, KeyError):
        raise ValueError("Parsing error, could not find the image source!")


def get_image_name(url_str: str) -> str:
    """
    :param url_str: http url of the image
    :return: the last element of the path
    """
    return urlparse(url_str).path.rsplit("/")[-1]


async def save_image(path_to_save: Path, img_name: str, img: bytes):
    if not path_to_save.exists():
        path_to_save.mkdir(parents=True)
    async with aiofiles.open(path_to_save / Path(img_name), mode="w+b") as fp:
        await fp.write(img)


async def download_image(path_to_save: Path, session: aiohttp.ClientSession):
    """
    Download image from https://www.thisfuckeduphomerdoesnotexist.com and
    save it to path_to_save

    :param path_to_save: absolute path where to save image
    :param session: aiohttp.ClientSession for making requests
    :return: None
    """
    async with session.get(url) as page_resp:
        img_url: str = find_img_url_from_html(await page_resp.text())
        imgfilename: str = get_image_name(img_url)
        async with session.get(img_url) as img_resp:
            if img_resp.status == 200:
                img: bytes = await img_resp.read()
                await save_image(path_to_save, imgfilename, img)


async def download_images(path_to_save: Path, images_count: int = 1):
    """
    Download images_count images from https://www.thisfuckeduphomerdoesnotexist.com and
    save it to path_to_save
    """
    assert images_count >= 1, "The minimal number of images to be downloaded is 1!"
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[download_image(path_to_save, session) for _ in range(images_count)])


async def main():
    parser = argparse.ArgumentParser(description=f"Download images from {url}")
    parser.add_argument(
        "-n",
        "--images_count",
        help="Number of images to be downloaded",
        default=1,
        type=int,
    )
    parser.add_argument(
        "-p",
        "--path",
        help="path to directory where to save images, by default images dir will be " "created in current directory",
        default=Path(os.getcwd()) / "thisfuckeduphomerdoesnotexist_imgs",
    )
    args = parser.parse_args()

    num_of_images = args.images_count
    location_to_save = args.path
    await download_images(location_to_save, num_of_images)


if __name__ == "__main__":
    asyncio.run(main())
