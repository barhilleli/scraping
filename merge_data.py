from __future__ import print_function
import glob
import cPickle


def main():
    visited_urls = []
    saved_urls = []
    for x in sorted(glob.glob('data/data*')):
        data = cPickle.load(open(x, 'rb'))
        saved_urls += data['saved_urls']
        visited_urls += data['visited_urls']

    saved_urls_unique = set(saved_urls)
    print('saved_urls len = {}'.format(len(saved_urls)))
    print('saved_urls_unique len = {}'.format(len(saved_urls_unique)))
    print(*saved_urls_unique,sep='\n')
    print('')

    visited_urls_unique = set(visited_urls)
    print('visited_urls len = {}'.format(len(visited_urls)))
    print('visited_urls_unique len = {}'.format(len(visited_urls_unique)))
    print('')


if __name__ == '__main__':
    main()