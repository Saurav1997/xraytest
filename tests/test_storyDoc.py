import pytest
from StoryDoc import StoryDoc

import logging

@pytest.fixture
def get_story ():
    return StoryDoc("J60_EXAMPLE[96].docx").get_story()

def test_epic(get_story):
    assert get_story["epic"] == 'PTP'

def test_story(get_story):
    assert get_story["userstory"] == "Accounts Payable (J60_US)"

def test_count_testsets (get_story):
    assert len(get_story['testsets']) == 2

def test_one_testset (get_story):
    assert get_story['testsets'][1]["name"] == 'Invoice Entry without Purchase Order'

def test_count_testcases (get_story):
    assert len(get_story['testsets'][0]['testcases']) + len(get_story['testsets'][1]['testcases']) == 7

def test_testcasename (get_story):
    assert (get_story['testsets'][1]['testcases'][2]['name']) == "Invoice Entry for One-Time Supplier without Purchase Order"

def test_teststepscheck (get_story):
    assert (get_story['testsets'][1]['testcases'][2]['steps'][7]["action"]) == "Post :: Choose the Post button."

