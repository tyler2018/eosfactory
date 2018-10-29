import unittest
from unittest import mock
from eosfactory.core.config import config_map, set_config, update_config


_existing_file_path = '/path/to/config/file'
_not_existing_file_path = '/path/to/file/which/not/exists'


def _os_path_exists(path):
    return  path == _existing_file_path


class config_map__Test(unittest.TestCase):

    def test__config_map_is_a_function(self):
        self.assertTrue(callable(config_map))

    @mock.patch('eosfactory.core.config.config_file', return_value=_existing_file_path)
    @mock.patch('os.path.exists', side_effect=_os_path_exists)
    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data='{"key":"value"}')
    def test__config_map__reads_from_config_file_if_config_exists(self, open_mock, file_exists_mock, config_file_mock):
        configuration = config_map()

        config_file_mock.assert_called_once_with()
        file_exists_mock.assert_called_once_with(_existing_file_path)
        open_mock.assert_called_once_with(_existing_file_path, "r")
        self.assertDictEqual(configuration, {"key": "value"})


    @mock.patch('eosfactory.core.config.config_file', return_value=_not_existing_file_path)
    @mock.patch('os.path.exists', side_effect=_os_path_exists)
    def test__config_map__if_config_file_does_not_exist_empty_dict_is_returned(self, file_exists_mock, config_file_mock):
        configuration = config_map()

        config_file_mock.assert_called_once_with()
        file_exists_mock.assert_called_once_with(_not_existing_file_path)
        self.assertDictEqual(configuration, {})

    @mock.patch('eosfactory.core.config.config_file', return_value=_existing_file_path)
    @mock.patch('os.path.exists', side_effect=_os_path_exists)
    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data='{"key":"value"}')
    def test__config_map__only_first_call_read_the_file(self, open_mock, file_exists_mock, config_file_mock):
        configuration = config_map()
        open_mock.assert_called_once_with(_existing_file_path, "r")
        self.assertDictEqual(configuration, {"key": "value"})

        configuration = config_map()
        open_mock.assert_called_once_with(_existing_file_path, "r")
        self.assertDictEqual(configuration, {"key": "value"})


    @mock.patch('eosfactory.core.config.config_file', return_value=_existing_file_path)
    @mock.patch('os.path.exists', side_effect=_os_path_exists)
    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data='{"key":"value"}')
    def test__config_map__you_cannot_change_configuration_implicitly(self, open_mock, file_exists_mock, config_file_mock):
        configuration = config_map()
        old_configuration = dict(configuration)
        configuration["new_item"] = "new_value"

        current_configuration = config_map()

        self.assertDictEqual(old_configuration, current_configuration)

    def tearDown(self):
        config_map.map = None


class set_config__Test(unittest.TestCase):

    def test__set_config_is_a_function(self):
        self.assertTrue(callable(set_config))

    @mock.patch('eosfactory.core.config.config_file', return_value=_existing_file_path)
    @mock.patch('os.path.exists', side_effect=_os_path_exists)
    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data='{"key":"value"}')
    def test__set_config__overrides_value_of_config_map(self, open_mock, file_exists_mock, config_file_mock):
        configuration = config_map()
        self.assertDictEqual(configuration, {"key": "value"})

        new_configuration = {"new_key": "new_value"}
        set_config(**new_configuration)
        configuration = config_map()
        self.assertDictEqual(configuration, new_configuration)

    def tearDown(self):
        config_map.map = None


class update_config__Test(unittest.TestCase):

    def test__update_config_is_a_function(self):
        self.assertTrue(callable(update_config))

    @mock.patch('eosfactory.core.config.config_file', return_value=_existing_file_path)
    @mock.patch('os.path.exists', side_effect=_os_path_exists)
    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data='{"key":"value", "key2": "value2"}')
    def test__update_config__add_and_overrides_values_in_config(self, open_mock, file_exists_mock, config_file_mock):
        configuration = config_map()
        self.assertDictEqual(configuration, {"key": "value", "key2": "value2"})

        new_configuration = {"key2": "value2a", "key3": "value3"}
        update_config(**dict(new_configuration))

        configuration.update(**new_configuration)
        current_configuration = config_map()
        self.assertDictEqual(configuration, current_configuration)

    def tearDown(self):
        config_map.map = None
