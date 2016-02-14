from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
from mrjob.step import MRStep
from Levenshtein import distance
import json
import scipy.stats
class MRTime(MRJob):

    def configure_options(self):
        super(MRTime, self).configure_options()
        self.add_file_option('--edit_distance_map')

    def mapper_init(self):
        words = set()
        with open(self.options.edit_distance_map) as op:
            self.the_dict = json.loads(op.read())

    def mapper(self, key, value):

        tmp = value[1:-1].split(",")
        l = [float(x) for x in tmp[3].split("\t")]
        print tmp[2]
        if self.the_dict.has_key(tmp[2]):
            print "Has Key"
            for word in self.the_dict.get(tmp[2]):
                print tmp[2]+"-->"+word
                yield word, l
            yield tmp[2], l

    def combiner(self, key, values):
        tmp = None
        for value in values:
            if tmp is None:
                tmp = value
            else:
                tmp = [x + y for x, y in zip(tmp, value)]
                tmp = [x / 2 for x in tmp]
        yield key, tmp


    def reducer(self, key, values):
        tmp = None
        for value in values:
            if tmp is None:
                tmp = value
            else:
                tmp = [x + y for x, y in zip(tmp, value)]
                tmp = [x / 2 for x in tmp]


        yield key, scipy.stats.spearmanr(tmp, range(0, len(tmp)))


    def steps(self):
        return [
            MRStep(mapper_init=self.mapper_init,
                   mapper=self.mapper,
                   combiner=self.combiner,
                   reducer=self.reducer)
        ]

if __name__ == '__main__':
    MRTime.run()
