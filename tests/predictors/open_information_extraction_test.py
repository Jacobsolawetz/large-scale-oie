
from allennlp.common.testing import AllenNlpTestCase
from allennlp.models.archival import load_archive
from allennlp.predictors import Predictor
from allennlp.data.tokenizers import WordTokenizer
from allennlp.data.tokenizers.word_splitter import SpacyWordSplitter

class TestOpenIePredictor(AllenNlpTestCase):
    def test_uses_named_inputs(self):
        """
        Tests whether the model outputs conform to the expected format.
        """
        inputs = {
                "sentence": "Angela Merkel met and spoke to her EU counterparts during the climate summit."
        }

        archive = load_archive(self.FIXTURES_ROOT / \
                               'srl' / 'serialization' / 'model.tar.gz')
        predictor = Predictor.from_archive(archive, 'oie')

        result = predictor.predict_json(inputs)

        words = result.get("words")
        assert words == ["Angela", "Merkel", "met", "and", "spoke", "to", "her", "EU", "counterparts",
                         "during", "the", "climate", "summit", "."]
        num_words = len(words)

        verbs = result.get("verbs")
        assert verbs is not None
        assert isinstance(verbs, list)

        for verb in verbs:
            tags = verb.get("tags")
            assert tags is not None
            assert isinstance(tags, list)
            assert all(isinstance(tag, str) for tag in tags)
            assert len(tags) == num_words


