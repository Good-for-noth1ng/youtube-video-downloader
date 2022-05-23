from typing import Pattern, Union

class RegexMatchError(Exception):
    def __init__(self, caller: str, pattern: Union[str, Pattern]):
        super().__init__(f"{caller} could'n find match {pattern}")
        self.caller = caller
        self.pattern = pattern

class VideoUnavailable(Exception):
    def __init__(self, video_id: str):
        self.video_id = video_id
        super().__init__(self.error_string)
    
    @property
    def error_string(self):
        return f"{self.video_id} is unavailable"

class AgeRestrictionError(VideoUnavailable):
    def __init__(self, video_id: str):
        self.video_id = video_id
        super().__init__(self.video_id)
    
    @property
    def error_string(self):
        return f"{self.video_id} is age restricted."

class LiveStreamError(VideoUnavailable):
    def __init__(self, video_id: str):
        self.video_id = video_id
        super().__init__(self.video_id)

    @property
    def error_string(self):
        return f"{self.video_id} is live stream broadcast"

class VideoIsPrivateError(VideoUnavailable):
    def __init__(self, video_id: str):
        self.video_id = video_id
        super().__init__(self.video_id)

    @property
    def error_string(self):
        return f"{self.video_id} is private"

class RecordingUnavailableError(VideoUnavailable):
    def __init__(self, video_id: str):
        self.video_id = video_id
        super().__init__(self.video_id)

    @property
    def error_string(self):
        return f"{self.video_id} doesn't have a live stream"

class MembersOnlyError(VideoUnavailable):
    def __init__(self, video_id: str):
        self.video_id = video_id
        super().__init__(self.video_id)

    @property
    def error_string(self):
        return f"{self.video_id} is a members only video"

class VideoRegionBlocked(VideoUnavailable):
    def __init__(self, video_id: str):
        self.video_id = video_id
        super().__init__(self.video_id)

    @property
    def error_string(self):
        return f"{self.video_id} isn't available in your region"