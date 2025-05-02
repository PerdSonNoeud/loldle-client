from champions import Champion, rdChamp
import constants as cons


class LoldleAPI:
    def __init__(self):
        self.champ = None
        self.guesses = []

    def start(self) -> None:
        """
        Function that start loldle.

        It initialise the base value of the champion to guess (random between
        all of them) and reset the number of tries (clear the history of
        guesses).
        """
        champ_dict = rdChamp()
        print("\tChampion aléatoire:", champ_dict["name"])
        self.champ = Champion(champ_dict)
        self.guesses = []

    def guess(self, champ: Champion) -> bool:
        """
        Function that checks if the champ is the right one
        """
        if self.champ.name == champ.name:
            self.guesses.insert(0, [cons.good, champ.name])
            return True
        else:
            self.guesses.insert(0, [cons.wrong, champ.name])
            return False

    def __str__(self):
        result = f"Nombre total d'essais : {len(self.guesses)}\n"
        for i in range(len(self.guesses)):
            if i >= 10:
                return result
            for info in self.guesses[i]:
                result += info + " "
            result += "\n"
        return result
