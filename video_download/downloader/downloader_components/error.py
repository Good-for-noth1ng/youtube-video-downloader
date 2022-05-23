from typing import Pattern, Union


class MaxRetriesError(Exception):
    pass

class HTMLParseError(Exception):
    """"""

class ExtractError(Exception):
    pass

class RegexMatchError(Exception):
    def __init__(self, caller: str, pattern: Union[str, Pattern]):
        super().__init__(f"{caller} could'n find match {pattern}")
        self.caller = caller
        self.pattern = pattern

class VideoUnavailableError(Exception):
    def __init__(self, video_id: str):
        self.video_id = video_id
        super().__init__(self.error_string)
    
    @property
    def error_string(self):
        return f"{self.video_id} is unavailable"

class AgeRestrictionError(VideoUnavailableError):
    def __init__(self, video_id: str):
        self.video_id = video_id
        super().__init__(self.video_id)
    
    @property
    def error_string(self):
        return f"{self.video_id} is age restricted."

class LiveStreamError(VideoUnavailableError):
    def __init__(self, video_id: str):
        self.video_id = video_id
        super().__init__(self.video_id)

    @property
    def error_string(self):
        return f"{self.video_id} is live stream broadcast"

class VideoIsPrivateError(VideoUnavailableError):
    def __init__(self, video_id: str):
        self.video_id = video_id
        super().__init__(self.video_id)

    @property
    def error_string(self):
        return f"{self.video_id} is private"

class RecordingUnavailableError(VideoUnavailableError):
    def __init__(self, video_id: str):
        self.video_id = video_id
        super().__init__(self.video_id)

    @property
    def error_string(self):
        return f"{self.video_id} doesn't have a live stream"

class MembersOnlyError(VideoUnavailableError):
    def __init__(self, video_id: str):
        self.video_id = video_id
        super().__init__(self.video_id)

    @property
    def error_string(self):
        return f"{self.video_id} is a members only video"

class VideoRegionBlocked(VideoUnavailableError):
    def __init__(self, video_id: str):
        self.video_id = video_id
        super().__init__(self.video_id)

    @property
    def error_string(self):
        return f"{self.video_id} isn't available in your region"