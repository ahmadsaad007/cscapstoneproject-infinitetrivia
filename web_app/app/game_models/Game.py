"""
Game
====
"""
import random

from .Player import Player
from .GameSettings import GameSettings
from trivia_generator.web_scraper.WebScraper import get_page_by_random
from trivia_generator.NLPPreProcessor import create_TUnits
from question_generator.NLPQuestionGeneratorSpacy import nlp_question_generation


class Game:
    """Class for a running instance of a game session. Contains All Game Logic.

    :param players: A list of the currently active players in the game.
    :param game_settings: A *GameSettings* object which contains the settings of the game.
    :param round_number: the current round number the game is on.
    :param game_code: the game code used to connect to the game.
    :param current_state: the current state of the game.
    :param game_states: a list of all possible game states.
    :param game_room: the ID of the game room used by connecting sockets.
    :param trivia_database: the database containing trivia questions.
    """
    # game_states: list

    def __init__(self, game_code: str,
                 game_settings: GameSettings,
                 host_id: str):
        self.players = []
        self.num_players = 0
        self.game_code = game_code
        self.game_settings = game_settings
        self.host_id = host_id
        self.round_number = 0
        self.current_state = "LOBBY"
        self.game_started = False
        self.current_trivia = ""
        self.number_of_responses = 0
        self.number_of_lies = 0
        self.current_answer = ""

    def add_player_to_lobby(self, player: Player) -> bool:
        """Adds a player to the current game lobby.

        :param player: the player to be added to the game lobby
        :type player: Player
        :returns: True if player was successfully added to lobby, False otherwise
        """
        if not self.game_started:
            self.players.append(player)
            self.num_players += 1
            return True
        else:
            return False

    def remove_player_from_lobby(self, player: Player) -> bool:
        """Removes a player from the current game lobby.

        :param player: the player to be removed from the game lobby
        :type player: Player
        :returns: True if player was successfully removed from lobby, False otherwise
        """
        self.players.remove(player)
        self.num_players -= 1
        return True

    def start_game(self) -> bool:
        """Finalizes the lobby and begins a game session.

        :returns: True if the game session was successfully started, false otherwise
        """
        self.game_started = True
        self.round_number = 1
        return True

    def get_round_number(self) -> int:
        """Returns the current game round.

        :returns: the current game round number as an integer
        """
        return self.round_number

    def get_score(self) -> dict:
        """creates and returns dictionary with the name and score of each player in game 

        :returns: a dictionary containinging the score of each player 
        """
        data = dict()
        data['players'] = []
        self.players.sort(key=lambda p: p.current_score, reverse=True)
        for player in self.players:
            player_entry = dict()
            player_entry['name'] = player.name
            player_entry['score'] = player.current_score
            data['players'].append(player_entry)
        return data

    def get_next_trivia(self) -> str:
        """Fetches a trivia question for the upcoming round from the trivia database, based on the current GameSettings.

        :returns: a trivia question
        """
        quest_ans_pairs = []
        print('searching for trivia!')
        while not quest_ans_pairs:
            trivia_article = get_page_by_random()
            tunit_list = create_TUnits(trivia_article)
            if tunit_list:
                tunit = random.choice(tunit_list)
                quest_ans_pairs = nlp_question_generation(tunit.sentence)
        trivia_question, trivia_answer = random.choice(quest_ans_pairs)
        print('found trivia!')
        self.current_trivia = trivia_question
        self.current_answer = trivia_answer
        return trivia_question

    def submit_answer(self, data: dict) -> list:
        """Retrives an answer the current trivia question from a given player.

        :returns: A list, the first values corresponding the the success of submitting
            the answer, true if successful, false otherwise,
            the second value is true if there are no players left to answer, false if there are
        
        """
        print("Game submission:", data)
        player = self.get_player_by_sid(data['sid'])
        if player is None:
            return [False, False]
        else:
            player.current_answer = data['answer']
            self.number_of_responses += 1
            print('number of responses:', self.number_of_responses)
            print('number of players:', self.num_players)
            if self.number_of_responses == self.num_players:
                return [True, True]
            return [True, False]

    def submit_lie(self, data: dict) -> list:
        """Retrives a lie submitted by a player in a fibbage game.

        :returns: A list, the first value corresponding to the success
        of submitting lie, the second corresponding to the if there are more players left to submit lies

        """
        player = self.get_player_by_sid(data['sid'])
        if player is None:
            return [False, False]
        player.current_lie = data['lie']
        print("submitted lie:", data['lie'])
        self.number_of_lies += 1
        print("number of lies:", self.number_of_lies)
        print('number of players:', self.num_players)
        if self.number_of_lies == self.num_players:
            return [True, True]
        return [True, False]

    def get_trivia_answer_and_responses(self) -> dict:

        """Returns the answer to the current trivia, and the responses of each player

        :returns: a dictionary containing the trivia answer, and player answers
        """
        data = dict()
        data['answer'] = self.current_answer
        self.players.sort(key=lambda p: p.name)
        data['player_answers'] = dict()
        for player in self.players:
            data['player_answers'][player.name] = dict()
            data['player_answers'][player.name]['answer'] = player.current_answer
            is_correct = (player.current_answer == self.current_answer)
            data['player_answers'][player.name]['correct'] = is_correct
            player.current_answer = ""
        self.round_number += 1
        self.update_scores(data)
        self.number_of_responses = 0
        return data

    def get_fibbage_answer_and_responses(self) -> dict:
        """Returns the answer to the current trivia, and the lies+answers of each player

        :returns: a dictionary containing the trivia answer, and the lie and answer of each player
        """
        data = dict()
        data['answer'] = self.current_answer
        data['players'] = []
        for player in self.players:
            player_info = dict()
            player_info['name'] = player.name
            player_info['answer'] = player.current_answer
            is_correct = (player.current_answer == self.current_answer)
            player_info['correct'] = is_correct
            player_info['lie'] = player.current_lie
            num_fooled = len([p.current_answer
                              for p in self.players
                              if p.current_answer == player.current_lie])
            player_info['fooled'] = num_fooled
            data['players'].append(player_info)
        self.round_number += 1
        # self.update_fibbage_scores(data) TODO
        self.number_of_responses = 0
        return data

    def get_fibbage_lies_and_answer(self) -> dict:
        """Returns all user-submitted lies to current fibbage trivia, and real answer 

        :returns: a dictionary containing the trivia answer, and player's lies
        """
        data = dict()
        data['answer'] = self.current_answer
        data['lies'] = []
        for player in self.players:
            lie = player.current_lie
            if lie != "":
                data['lies'].append(lie)
                #  player.current_lie = ""
                #  self.numer_of_lies = 0
        return data

    def update_fibbage_scores(self, data):
        """Updates the scores of each player based on the answer and lies of each player"""
        pass

    def update_scores(self, data):
        """Updates the scores of each player based on the data of each player."""
        for player in self.players:
            if data['player_answers'][player.name]['correct']:
                # TODO determine how many points they should get
                player.update_score(1)

    def submit_trivia_rank(self, rank):
        # TODO
        # 1. find current trivia TUnit
        # 2. update TUnit in DB based on rank
        print("trivia recieved rank", rank)

    def display_category_options(self) -> bool:
        """If applicable (depending on game mode), send a list of possible categories that a player can choose from to the front end, which will be displayed to the selected user.

        :returns: True if categories were properly fetched from database and sent to frontend, False otherwise
        """
        pass

    def determine_winners_of_round(self):
        """Based of off the current trivia and the received answers from each player, determine who won the round.
        """
        pass

    def prompt_for_lie(self) -> bool:
        """If applicable (depending on game mode), tell front-end to prompt all player(s) for a fake-answer to a trivia question.

        :returns: True if info was successfully sent to front-end, False otherwise
        """
        pass

    def finish_game(self) -> bool:
        """After all rounds have been completed, sents "credits" information to front-end and updates statistics for all registered users.
        
        :returns: True if info was successfully sent to front-end and user statistics were updated, false otherwise
        """
        pass

    def get_player_by_sid(self, sid: str) -> Player:
        """Returns the given player in game based off of their SID, or None if not found.

        :returns: The player corresponding to the given SID, or None if not found
        """
        for player in self.players:
            if sid == player.ID:
                return player
        return None
