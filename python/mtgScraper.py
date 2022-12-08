from matchRecord import MatchRecord
import os
import argparse


def main(path, player):
    file_list = [f for f in os.listdir(path) if f.endswith('.dat')]
    match = MatchRecord(player=player)
    for filename in file_list:
        match.run(f'{path}/{filename}')
    match.quit()
    
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='mtgo_scraper')
    parser.add_argument('--player', nargs='?', default=None)
    parser.add_argument('path', nargs=1, type=str, default='.', help='Path to data folder.')
    args = parser.parse_args()
    print('Running...')
    main(args.path[0], args.player)
