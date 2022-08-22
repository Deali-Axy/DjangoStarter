from typing import Optional


class LoginResult(object):
    """登录结果"""

    def __init__(
            self, is_successful: bool,
            user_data: Optional[dict] = None,
            profile_data: Optional[dict] = None,
            token: Optional[str] = None
    ):
        """

        :param is_successful: 是否成功
        :param user_data: 用户数据，使用 Serializer 序列化
        :param profile_data: 用户资料数据，使用 Serializer 序列化
        :param token:
        """
        self.is_successful = is_successful
        self.user_data = user_data
        self.profile_data = profile_data
        self.token = token

    def to_dict(self):
        return {
            'user': self.user_data,
            'profile': self.profile_data,
            'token': self.token
        }
