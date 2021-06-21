import pytest
import yaml
import logging
import re
import json

from xray import JiraXray as JX

@pytest.fixture
def xray_settings ():
    env = "test"
    settings = yaml.load(open('settings.yml','r'), Loader = yaml.CLoader)[env]
    return {
        "client_id":settings["xray"]["clientid"],
        "client_secret":settings["xray"]["secret"],
    }

def test_settings(xray_settings):
    assert xray_settings["client_id"] == "166906E845714AF09E677D197363B786"

def test_login(xray_settings,caplog):
    caplog.set_level (logging.INFO)
    jx = JX.JiraXray (xray_settings)
    assert jx.status_code == 200

def test_get_tests(xray_settings):
    jx = JX.JiraXray(xray_settings)

    
def test_run_graphql_query(xray_settings):
    jx = JX.JiraXray(xray_settings)
    query = """query {
        __type(name: "Test") {
            name
            kind
            description
            fields {
                name
            }
        }
    }"""
    print (jx.run_graphql_query(query))
    assert False