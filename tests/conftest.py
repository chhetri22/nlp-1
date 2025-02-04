# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# NOTE: This file is used by pytest to inject fixtures automatically.
# As it is explained in the documentation
# https://docs.pytest.org/en/latest/fixture.html:
# "If during implementing your tests you realize that you want to use
# a fixture function from multiple test files you can move it to a conftest.py
# file. You don’t need to import the fixture you want to use in a test, it
# automatically gets discovered by pytest."

import os
from tempfile import TemporaryDirectory

import pytest
from tests.notebooks_common import path_notebooks

from utils_nlp.models.bert.common import Language as BERTLanguage
from utils_nlp.models.xlnet.common import Language as XLNetLanguage
from utils_nlp.models.bert.common import Tokenizer as BERTTokenizer
from utils_nlp.models.xlnet.common import Tokenizer as XLNetTokenizer
from utils_nlp.azureml import azureml_utils
from azureml.core.webservice import Webservice


@pytest.fixture(scope="module")
def notebooks():
    folder_notebooks = path_notebooks()

    # Path for the notebooks
    paths = {
        "embedding_trainer": os.path.join(
            folder_notebooks, "embeddings", "embedding_trainer.ipynb"
        ),
        "similarity_embeddings_baseline": os.path.join(
            folder_notebooks, "sentence_similarity", "baseline_deep_dive.ipynb"
        ),
        "bert_encoder": os.path.join(folder_notebooks, "sentence_similarity", "bert_encoder.ipynb"),
        "gensen_local": os.path.join(folder_notebooks, "sentence_similarity", "gensen_local.ipynb"),
        "gensen_azureml": os.path.join(
            folder_notebooks, "sentence_similarity", "gensen_aml_deep_dive.ipynb"
        ),
        "similarity_automl_local": os.path.join(
            folder_notebooks, "sentence_similarity", "automl_local_deployment_aci.ipynb"
        ),
        "automl_with_pipelines_deployment_aks": os.path.join(
            folder_notebooks, "sentence_similarity", "automl_with_pipelines_deployment_aks.ipynb"
        ),
        "bert_qa_trainer": os.path.join(
            folder_notebooks, "question_answering", "pretrained-BERT-SQuAD-deep-dive-aml.ipynb"
        ),
        "bidaf_deep_dive": os.path.join(
            folder_notebooks, "question_answering", "bidaf_aml_deep_dive.ipynb"
        ),
        "bidaf_quickstart": os.path.join(
            folder_notebooks,
            "question_answering",
            "question_answering_system_bidaf_quickstart.ipynb",
        ),
        "entailment_multinli_bert": os.path.join(
            folder_notebooks, "entailment", "entailment_multinli_bert.ipynb"
        ),
        "entailment_bert_azureml": os.path.join(
            folder_notebooks, "entailment", "entailment_xnli_bert_azureml.ipynb"
        ),
        "tc_bert_azureml": os.path.join(
            folder_notebooks, "text_classification", "tc_bert_azureml.ipynb"
        ),
        "bert_senteval": os.path.join(
            folder_notebooks, "sentence_similarity", "bert_senteval.ipynb"
        ),
        "tc_mnli_bert": os.path.join(folder_notebooks, "text_classification", "tc_mnli_bert.ipynb"),
        "ner_wikigold_bert": os.path.join(
            folder_notebooks, "named_entity_recognition", "ner_wikigold_bert.ipynb"
        ),
        "deep_and_unified_understanding": os.path.join(
            folder_notebooks, "model_explainability", "interpret_dnn_layers.ipynb"
        ),
    }
    return paths


@pytest.fixture
def tmp(tmp_path_factory):
    td = TemporaryDirectory(dir=tmp_path_factory.getbasetemp())
    try:
        yield td.name
    finally:
        td.cleanup()


@pytest.fixture(scope="module")
def ner_test_data():
    UNIQUE_LABELS = ["O", "I-LOC", "I-MISC", "I-PER", "I-ORG", "X"]
    LABEL_MAP = {label: i for i, label in enumerate(UNIQUE_LABELS)}
    TRAILING_TOKEN_MASK = [[True] * 20]
    false_pos = [1, 2]
    for p in false_pos:
        TRAILING_TOKEN_MASK[0][p] = False
    INPUT_LABEL_IDS = [[3, 5, 5, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    return {
        "INPUT_TEXT": [
            ["Johnathan", "is", "studying", "in", "the", "University", "of", "Michigan", "."]
        ],
        "INPUT_TEXT_SINGLE": [
            "Johnathan",
            "is",
            "studying",
            "in",
            "the",
            "University",
            "of",
            "Michigan",
            ".",
        ],
        "INPUT_LABELS": [["I-PER", "O", "O", "O", "O", "I-ORG", "I-ORG", "I-ORG", "O"]],
        "INPUT_LABELS_SINGLE": ["I-PER", "O", "O", "O", "O", "I-ORG", "I-ORG", "I-ORG", "O"],
        "INPUT_LABELS_WRONG": [["I-PER", "O", "O", "O", "O", "I-ORG", "I-ORG", "I-ORG"]],
        "INPUT_TOKEN_IDS": [
            [
                1287,
                9779,
                1389,
                1110,
                5076,
                1107,
                1103,
                1239,
                1104,
                3312,
                119,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
            ]
        ],
        "INPUT_LABEL_IDS": INPUT_LABEL_IDS,
        "INPUT_MASK": [[1] * 11 + [0] * 9],
        "PREDICTED_LABELS": [[3, 5, 5, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "TRAILING_TOKEN_MASK": TRAILING_TOKEN_MASK,
        "UNIQUE_LABELS": UNIQUE_LABELS,
        "LABEL_MAP": LABEL_MAP,
        "EXPECTED_TOKENS_NO_PADDING": [
            ["I-PER", "X", "X", "O", "O", "O", "O", "I-ORG", "I-ORG", "I-ORG", "O"]
        ],
        "EXPECTED_TOKENS_NO_PADDING_NO_TRAILING": [
            ["I-PER", "O", "O", "O", "O", "I-ORG", "I-ORG", "I-ORG", "O"]
        ],
        "EXPECTED_TRAILING_TOKEN_MASK": TRAILING_TOKEN_MASK,
        "EXPECTED_LABEL_IDS": INPUT_LABEL_IDS,
    }


def pytest_addoption(parser):
    parser.addoption("--subscription_id", help="Azure Subscription Id to create resources in")
    parser.addoption("--resource_group", help="Name of the resource group")
    parser.addoption("--workspace_name", help="Name of Azure ML Workspace")
    parser.addoption("--workspace_region", help="Azure region to create the workspace in")
    parser.addoption("--cluster_name", help="Name of the AzureML Cluster.")


@pytest.fixture(scope="module")
def subscription_id(request):
    return request.config.getoption("--subscription_id")


@pytest.fixture(scope="module")
def resource_group(request):
    return request.config.getoption("--resource_group")


@pytest.fixture(scope="module")
def workspace_name(request):
    return request.config.getoption("--workspace_name")


@pytest.fixture(scope="module")
def workspace_region(request):
    return request.config.getoption("--workspace_region")


@pytest.fixture(scope="module")
def cluster_name(request):
    return request.config.getoption("--cluster_name")


@pytest.fixture()
def bert_english_tokenizer():
    return BERTTokenizer(language=BERTLanguage.ENGLISHCASED, to_lower=False)

@pytest.fixture()
def xlnet_english_tokenizer():
    return XLNetTokenizer(language=XLNetLanguage.ENGLISHCASED)


@pytest.fixture(scope="module")
def teardown_service(subscription_id, resource_group, workspace_name, workspace_region):

    yield

    # connect to workspace
    ws = azureml_utils.get_or_create_workspace(
        config_path="tests/ci",
        subscription_id=subscription_id,
        resource_group=resource_group,
        workspace_name=workspace_name,
        workspace_region=workspace_region,
    )

    # connect to aci_service
    aci_service = Webservice(workspace=ws, name="aci-test-service")

    # delete aci_service
    aci_service.delete()
