import requests
import logging
import base64
import json
from pprint import pformat
import re

class JiraXray:
    def __init__(self, settings):
        self.resturl = 'https://xray.cloud.xpand-it.com/'
        self.xrayurl = 'https://xray.cloud.xpand-it.com/api/v2/graphql'
        self.auth_json = {"client_id": settings["client_id"], "client_secret": settings["client_secret"]}
        logging.getLogger().debug (self.auth_json)
        response = requests.post (self.resturl + 'api/v1/authenticate' , json = self.auth_json)
        self.status_code = response.status_code
        self.headers = {'Authorization': f'Bearer {response.json()}'}
        if response.status_code != 200:
            logging.getLogger().info (str(response.status_code))
            logging.getLogger().info (response.json())
        else:
            logging.getLogger().debug (self.headers)

    def run_graphql_query (self,query):
        logging.getLogger().debug(query)
        response = requests.post(f"{self.xrayurl}", headers = self.headers, json = {'query': query})
        self.response_code = response.status_code
        if response.status_code == 200:
            logging.getLogger().debug(response.text)
            return json.loads(response.text)['data']
        else:
            logging.getLogger().info(query)
            logging.getLogger().info(response.text)
            #logging.getLogger().info(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
            raise Exception (f"GraphQL Query failed with Error Code {self.response_code}")

    def get_tests (self, jql):
        query = f""" query {{
            getTests(jql: "{jql}", limit: 100) {{
                total
                results {{
                    issueId
                    testSets (limit: 10) {{
                        total
                        results {{
                            issueId
                            jira (fields: ["key"])
                        }}
                    }}
                    jira(fields: ["key","labels"])
                }}
            }}
        }}"""
        return (self.run_graphql_query(query))

    def get_test_sets(self,project, start):
        jql = f"project = '{project}'"
        query = f"""query {{
            getTestSets(jql: "{jql}", limit: 100, start: {start}) {{
                total
                start
                limit
                results {{
                    issueId
                    jira(fields: ["key"])
                }}
            }}
        }}"""
        return (self.run_graphql_query(query))

    def get_testset_id (self, key):
        jql = f"key = '{key}'"
        query = f"""query {{
            getTestSets(jql: "{jql}", limit: 1) {{
                total
                results {{
                    issueId
                }}
            }}
        }}"""
        return (self.run_graphql_query(query)["getTestSets"]["results"][0]["issueId"])

    def add_tests_to_set (self, setid, tests):
        query = f"""mutation {{
            addTestsToTestSet(
            issueId: "{setid}",
            testIssueIds: {tests}
            ) {{
                addedTests
                warning
            }}
        }}"""
        logging.info(self.run_graphql_query(query))