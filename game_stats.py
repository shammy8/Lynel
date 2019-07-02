class GameStats():

    def __init__(self, ai_settings):
        """puts the game in pause mode at the start, load the high score from text file. """
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        f = open("highscore.txt","r")
        self.high_score = int(f.read())
        f.close()

    def reset_stats(self):
        """after Link loses all his lifes, restarts the score, level, scoring multiplier"""
        self.link_left = self.ai_settings.link_lifes
        self.score = 0
        self.level = 1
        self.multiplier = 1

    def update_highscore(self):
        """updates the high score to a text file when the game is closed, to be loaded next time game is loaded"""
        f = open("highscore.txt","w")
        f.write(str(self.high_score))
        f.close()

    