import asyncio
import json
import os
import time

import challonge

from config import config
from commands.mid_man  import mid_man



def tournament(tournName, server_list, matchIndex):


    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    loop = asyncio.get_event_loop()
    challonge.set_credentials(config.CHAL_USER, config.CHAL_API)


    if '{}' in str(matchIndex):
        matchIndex = challonge.matches.index(tournName)
        print('matchIndex empty, recreating..')
    newMatchIndex = challonge.matches.index(tournName)

    iteration = 0
    change = False
    for gameNew in newMatchIndex:
        for gameOld in matchIndex:
            if gameOld['identifier'] == gameNew['identifier']:
                #print('Matched game {}'.format(gameOld['identifier']))
                if 'None' in str(gameNew['winner-id']):
                    if (gameNew['player1-id'] != gameOld['player1-id'] or
                     gameNew['player2-id'] != gameOld['player2-id']):
                        if ('None' not in str(gameNew['player1-id']) and
                            'None' not in str(gameNew['player2-id'])):
                            tournament = challonge.tournaments.show(gameNew['tournament-id'])
                            player1 = challonge.participants.show(tournament['name'], gameNew['player1-id'])
                            player2 = participant = challonge.participants.show(tournament['name'], gameNew['player2-id'])

                            newMatchString = ('Match beginning: ```\n{} VS. {}\n\n'
                            'All players please report to tournament rooms within '
                            '30 minutes.\nIf there are any issue please seek a LAG'
                            ' staff member.```'.format(player1['name'], player2['name']))

                            loop.create_task(mid_man(newMatchString, server_list))
                elif ('None' not in str(gameNew['winner-id']) and
                        gameNew['winner-id'] != gameOld['winner-id']):

                    tournament = challonge.tournaments.show(gameNew['tournament-id'])
                    winner = challonge.participants.show(tournament['name'], gameNew['winner-id'])
                    loser = participant = challonge.participants.show(tournament['name'], gameNew['loser-id'])
                    change = True

                    matchWinStr = ('Match has been won!\n```Tournament: {}'
                            '\nWinner : {}\nLoser : {}```'.format(tournament['name'],
                             winner['name'], loser['name']))

                    print(matchWinStr)
                    loop.create_task(mid_man(matchWinStr, server_list))

    if change == True:
        return newMatchIndex
    else:
        return matchIndex
