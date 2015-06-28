from collections import defaultdict
from datetime import datetime
import random
import sys
import time


class MarkovMuse(object):
    def __init__(self, posts, min_date, max_date, muse_length=250):
        self.min_date, self.max_date = self._validate_dates(min_date, max_date)
        self.words = self._posts_to_words(posts)
        self.bigram_lookup = self._create_bigram_lookup()
        self.muse_length = muse_length

    @staticmethod
    def _validate_dates(min_date, max_date):
        if not (isinstance(min_date, datetime) and isinstance(min_date, datetime)):
            min_date = datetime.strptime(min_date, '%Y-%m-%d')
            max_date = datetime.strptime(max_date, '%Y-%m-%d')
        return min_date, max_date

    @staticmethod
    def _tokenize_post(post):
        return [word.strip() for word in post.split() if word.strip() != '']

    @staticmethod
    def _yield_trigrams(words):
        for i in range(len(words) - 3):
            yield (words[i], words[i+1], words[i+2])

    def _posts_to_words(self, posts):
        words = []
        for post in posts:
            if post['date'] >= self.min_date and post['date'] <= self.max_date:
                words.extend(self._tokenize_post(post['text']))
        if len(words) == 0:
            sys.exit('No posts between the specified dates - please try new dates.')
        return words

    def _create_bigram_lookup(self):
        lookup = defaultdict(list)
        for w1, w2, w3 in self._yield_trigrams(self.words):
            lookup[(w1, w2)].append(w3)
        return lookup

    def _generate(self, muse_length):
        muse = ''
        seed = random.randint(0, len(self.words) - 2)
        w1, w2 = self.words[seed], self.words[seed + 1]

        while len(muse.split()) < muse_length:
            muse += (w1 + ' ')
            w1, w2 = w2, random.choice(self.bigram_lookup[(w1, w2)])

        return muse

    def generate(self):
        # for effect ..
        print('\nGenerating your post ...\n')
        time.sleep(1.5)

        muse_title = self._generate(10).strip(' ,.?!').title()
        muse = self._generate(self.muse_length)

        # cleanup
        muse = muse.strip(' ,')
        muse = muse[0].upper() + muse[1:]
        if muse[-1] not in '.?!':
            muse += random.choice('.?!')

        muse = muse_title + ':\n\n' + muse
        return muse


if __name__ == '__main__':
    from posts import posts

    min_date = input('Please input a min_date in the form \'YYYY-MM-DD\': ')
    max_date = input('Please input a max_date in the form \'YYYY-MM-DD\': ')
    muse_length = input('Please input the desired length of the post to be produced: ')
    muse_length = muse_length if isinstance(muse_length, int) else 250

    markov_muse = MarkovMuse(
        posts=posts,
        min_date=min_date,
        max_date=max_date,
        muse_length=muse_length
    )

    print(markov_muse.generate())
