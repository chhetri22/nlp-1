# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import sys
import pytest
import papermill as pm
import scrapbook as sb
from tests.notebooks_common import OUTPUT_NOTEBOOK

ABS_TOL = 0.2

@pytest.mark.notebooks
def test_bidaf_deep_dive(notebooks):
    notebook_path = notebooks["bidaf_deep_dive"]
    pm.execute_notebook(notebook_path,
                        OUTPUT_NOTEBOOK,
                        parameters = {'NUM_EPOCHS':2,
                                      'config_path': "tests/ci",
                                      'PROJECT_FOLDER': "scenarios/question_answering/bidaf-question-answering",
                                      'SQUAD_FOLDER': "scenarios/question_answering/squad",
                                      'LOGS_FOLDER': "scenarios/question_answering/",
                                      'BIDAF_CONFIG_PATH': "scenarios/question_answering/"})
    result = sb.read_notebook(OUTPUT_NOTEBOOK).scraps.data_dict["validation_EM"]
    assert result == pytest.approx(0.5, abs=ABS_TOL)

@pytest.mark.notebooks
def test_bidaf_quickstart(notebooks):
    notebook_path = notebooks["bidaf_quickstart"]
    pm.execute_notebook(notebook_path,
                        OUTPUT_NOTEBOOK,
                        parameters = {'config_path': "tests/ci"})
    result = sb.read_notebook(OUTPUT_NOTEBOOK).scraps.data_dict["answer"]
    assert result == "Bi-Directional Attention Flow"