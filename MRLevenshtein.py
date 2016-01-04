from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
from mrjob.step import MRStep
from Levenshtein import distance

class MRLevenshtein(MRJob):

    def configure_options(self):
        super(MRLevenshtein, self).configure_options()
        self.add_file_option('--wordlist')

    def mapper_init(self):
        self.wordlist = [line.rstrip('\n') for line in open(self.options.wordlist)]

    def mapper(self, key, value):
        for word in self.wordlist:
            dist = distance(word, value)
            yield key, "{} {}".format(word, str(dist))

    def steps(self):
        return [
            MRStep(mapper_init=self.mapper_init,
                   mapper=self.mapper)
        ]

if __name__ == '__main__':
    MRLevenshtein.run()
