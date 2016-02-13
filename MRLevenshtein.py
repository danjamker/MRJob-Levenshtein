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
            if dist <= 2:
                yield word, value

    def reducer(self, key, values):
        s = []
        for st in values:
            s.append(st)

        yield key, " ".join(s)

    def steps(self):
        return [
            MRStep(mapper_init=self.mapper_init,
                   mapper=self.mapper,
                   reducer=self.reducer)
        ]

if __name__ == '__main__':
    MRLevenshtein.run()
