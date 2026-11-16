
import re

def get_video_id(url: str) -> str:
    patterns = [
        r"(?:youtube\.com/watch\?v=)([A-Za-z0-9_-]{11})",
        r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:youtube\.com/embed/)([A-Za-z0-9_-]{11})",
        r"(?:youtube\.com/shorts/)([A-Za-z0-9_-]{11})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    raise ValueError("Please enter a valid public YouTube video URL.")


def get_transcript(url: str) -> str:
    video_id = get_video_id(url)

    from youtube_transcript_api import YouTubeTranscriptApi

    api = YouTubeTranscriptApi()

    try:
        # Try English first, then Hindi
        transcript = api.fetch(video_id, languages=["en", "hi"])

        return "\n".join(
            item.text for item in transcript
        )

    except Exception as error:
        raise ValueError(
            "Could not retrieve captions in English or Hindi. "
            "Please check whether captions are available for this video. "
            f"Details: {error}"
        )
