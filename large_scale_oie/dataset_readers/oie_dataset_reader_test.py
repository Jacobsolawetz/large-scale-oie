# pylint: disable=no-self-use,invalid-name
from allennlp.common.testing import AllenNlpTestCase
from allennlp.common.util import ensure_list

from oie_reader import OieReader






class TestOieDatasetReader(AllenNlpTestCase):
    def test_read_from_file(self):

        reader = OieReader()
        #test data directory listed below. OieReader loops through the files therein and loads.
        instances =  ensure_list(reader._read('onto_notes_conlls'))
        fields = instances[0].fields
        print([t.text for t in fields["tokens"].tokens])
        print([l for l in fields["tags"].labels])
        #print([t.text for t in fields["verb_indicator"].tokens])
        #print([t.text for t in fields["metadata"].tokens])
        fields = instances[1].fields
        print([t.text for t in fields["tokens"].tokens])
        print([l for l in fields["tags"].labels])

        fields = instances[2].fields
        print([t.text for t in fields["tokens"].tokens])
        print([l for l in fields["tags"].labels])

        fields = instances[3].fields
        print([t.text for t in fields["tokens"].tokens])
        print([l for l in fields["tags"].labels])

        fields = instances[4].fields
        print([t.text for t in fields["tokens"].tokens])
        print([l for l in fields["tags"].labels])

'''
        assert len(instances) == 10
        fields = instances[0].fields
        assert [t.text for t in fields["title"].tokens] == instance1["title"]
        assert [t.text for t in fields["abstract"].tokens[:5]] == instance1["abstract"]
        assert fields["label"].label == instance1["venue"]
        fields = instances[1].fields
        assert [t.text for t in fields["title"].tokens] == instance2["title"]
        assert [t.text for t in fields["abstract"].tokens[:5]] == instance2["abstract"]
        assert fields["label"].label == instance2["venue"]
        fields = instances[2].fields
        assert [t.text for t in fields["title"].tokens] == instance3["title"]
        assert [t.text for t in fields["abstract"].tokens[:5]] == instance3["abstract"]
        assert fields["label"].label == instance3["venue"]

        '''



if __name__ == "__main__":
    tester = TestOieDatasetReader()
    tester.test_read_from_file()

