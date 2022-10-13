from matchRecord import matchRecord
import os
import argparse


def main(path, player):
    file_list = [f for f in os.listdir(path) if f.endswith('.dat')]
    records = list()
    for filename in file_list:
        #print(filename)
        matchRecord(f'{path}/{filename}', player=player)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='mtgo_scraper',
        description='''Read all mtgo logfiles from specified
        folder and compile the information into a json.''')
    parser.add_argument('--player', nargs='?', default=None)
    parser.add_argument('path', nargs=1, type=str, default='.',
                        help='Path to data folder.')
    args = parser.parse_args()
    #print(args)
    print('Running...')
    main(args.path[0], args.player)
