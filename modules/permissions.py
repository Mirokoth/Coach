from config import config

class AccessController():

    def __init__(self, coach):
        self.coach = coach

    def isAdmin(self, user):
        """ Determine if a user is an administrator

        Args:
            server (string):    Discord server ID
            user (string):      Discord user ID

        Returns:
            bool:   True is admin, False is not.

        """
        for role in user.roles:
            for adminRole in config.adminRoleIds:
                if role.id == adminRole:
                    return True
        # No match
        return False
