import os

class ManifestManager:
    def __init__(self):
        self.manifests_dir = os.environ.get('MANIFESTS_DIR', 'manifests')

    def list_games(self):
        games = []
        for game in os.listdir(self.manifests_dir):
            if os.path.isdir(os.path.join(self.manifests_dir, game)):
                games.append(game)

        return games

    def list_game_versions(self, game_name):
        game_versions = []

        game_dir = os.path.join(self.manifests_dir, game_name)
        if not game_dir:
            return False
        
        for version in os.listdir(game_dir):
            version_name = os.path.splitext(version)[0]
            game_versions.append(version_name)

        return game_versions


# # Needs to be able to
# # - Read manifest dir
# # - Configure manifests 

_manifestManager = ManifestManager()

def list_games():
    return _manifestManager.list_games()

def list_game_versions(game_name: str):
    return _manifestManager.list_game_versions(game_name)