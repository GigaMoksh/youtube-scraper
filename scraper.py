from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

YOUTUBE_TRENDING_URL = "https://www.youtube.com/feed/trending"


def get_driver():  # sourcery skip: inline-immediately-returned-variable
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_videos(driver):  # sourcery skip: inline-immediately-returned-variable
    driver.get(YOUTUBE_TRENDING_URL)
    print("Page title: ", driver.title)
    VIDEO_TAG = "ytd-video-renderer"
    videos = driver.find_elements(By.TAG_NAME, VIDEO_TAG)
    return videos


def parse_video(video):
    title_tag = video.find_element(By.ID, "video-title")
    title = title_tag.text
    URL = title_tag.get_attribute("href")

    thumbnail_tag = video.find_element(By.TAG_NAME, "img")
    thumbnail_url = thumbnail_tag.get_attribute("src")

    channel_tag = video.find_element(By.CLASS_NAME, "ytd-channel-name")
    channel_name = channel_tag.text

    view_uploaded_time_tag = video.find_element(By.ID, "metadata-line")
    views, uploaded_time, _ = view_uploaded_time_tag.find_elements(
        By.CLASS_NAME, "ytd-video-meta-block"
    )
    views = views.text
    uploaded_time = uploaded_time.text

    description_tag = video.find_element(By.ID, "description-text")
    description = description_tag.text

    return {
        "title": title,
        "url": URL,
        "thumbnail_url": thumbnail_url,
        "channel": channel_name,
        "views": views,
        "uploaded_time": uploaded_time,
        "description": description,
    }


if __name__ == "__main__":
    driver = get_driver()
    videos = get_videos(driver)

    videos_data = [parse_video(video) for video in videos[:10]]
    videos_df = pd.DataFrame(videos_data)
    videos_df.to_csv("trending.csv", index=None)

