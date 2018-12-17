# pylint: disable=invalid-name,protected-access
from allennlp.common.testing import ModelTestCase


class OieLabelerTest(ModelTestCase):
    def setUp(self):
        super(OieLabelerTest, self).setUp()
        #(config_path, data_path)
        self.set_up_model('tests/fixtures/oie_labeler.json',
                          'tests/fixtures')

    def test_model_can_train_save_and_load(self):
        self.ensure_model_can_train_save_and_load(self.param_file)
