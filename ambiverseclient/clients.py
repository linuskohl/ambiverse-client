# -*- coding: utf-8 -*-
import json
import requests
from typing import Union
from requests.exceptions import InvalidURL
from urllib.parse import urlencode, urljoin
from .models import *

__author__ = "Linus Kohl"

class __BaseClient(object):

    def __init__(self, hostname: str, port: int = 80, path: str = None, protocol: str = "http"):
        """
        Args:
            hostname (str): Hostname
            port (int): Port
            path (str): Subpath of the endpoint
            protocol (str): Protocol to use (http|https)
        Raises:
            InvalidUrl: If hostname is not set
        """
        if None in [hostname]:
            raise InvalidURL
        self.__api_base_url = "{scheme}://{hostname}:{port}/{path}".format(
            scheme=protocol,
            hostname=hostname,
            port=str(port or ''),
            path=str(path or '')
        )

    def call(self, path: str, method: str = 'GET', status: int = 200, data: dict = None) -> Dict:
        """Call the API endpoint
        Args:
            path (str): The URL path to call
            method (str): HTTP method [GET, POST]
            status (int): Successful response code (defaults to 200)
            data (dict): Dictionary containing the body of the request
        Returns:
            dict: loaded body of the response
        Raises:
            Exception: If response code is not equal to set status code
        """
        # set headers
        headers = {}
        headers["Content-Type"] = "application/json"
        # build url
        url = self.__api_base_url + path
        # encode payload
        encoded = json.dumps(data)
        # send request
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, data=encoded, headers=headers)
        if response.status_code != status:
            raise Exception("Wrong HTTP response code")
        resp_dict = json.loads(response.content)

        return resp_dict

    def marshall(self, schema: Schema, data_dict: dict):
        """ Load object from dict
        Args:
            schema (Schema): Hostname
            data_dict (dict): Dict containing data to loda
        """
        return schema.load(data_dict)


class KnowledgeGraph(__BaseClient):
    BASE_PATH = "knowledgegraph"

    def __init__(self, hostname: str, port: int = 80, path: str = None, protocol: str = "http"):
        """
        Args:
            hostname (str): Hostname
            port (int): Port
            path (str): Subpath of the endpoint
            protocol (str): Protocol to use (http|https)
        """
        path = urljoin(path, self.BASE_PATH).strip("/")
        super().__init__(hostname, port, path, protocol)

    def entities(self, entity_identifiers: list, raw: bool = False) -> Union[List[Entity], Dict]:
        """Get entities of knowledge graph
        Args:
            entity_identifiers (list): List containing entitiy identifiers
            raw (bool): If True return raw dict
        Returns:
            dict: unprocessed result
            List[Entity]: processed result
        Raises:
            Exception: If response code is not equal to set status code
        """
        if not isinstance(entity_identifiers, list):
            raise Exception
        response = self.call("/entities", method="POST", status=200, data=entity_identifiers)
        if raw == False:
            return self.marshall(EntitiesSchema(), response)
        else:
            return response

    def entities_meta(self, raw: bool = False) -> Union[Meta, Dict]:
        """Get meta information of the endpoint
        Args:
            raw (bool): If True return raw dict
        Returns:
            dict: unprocessed result
            Meta: processed result
        Raises:
            Exception: If response code is not equal to set status code
        """
        response = self.call("/entities/_meta", method="GET", status=200)
        if raw == False:
            return self.marshall(MetaSchema(), response)
        else:
            return response

    def categories(self, entity_identifiers: list, raw: bool = False) -> Union[List[Category], Dict]:
        """Get categories of knowledge graph
        Args:
            entity_identifiers (list): List containing entitiy identifiers
            raw (bool): If True return raw dict
        Returns:
            dict: unprocessed result
            List[Category]: processed result
        Raises:
            Exception: If response code is not equal to set status code
        """
        if not isinstance(entity_identifiers, list):
            raise Exception
        response = self.call("/categories", method="POST", status=200, data=entity_identifiers)
        if raw == False:
            return self.marshall(CategoriesSchema(), response)
        else:
            return response

    def categories_meta(self, raw: bool = False) -> Union[Meta, Dict]:
        """Get meta information of endpoint
        Args:
            raw (bool): If True return raw dict
        Returns:
            dict: unprocessed result
            Meta: processed result
        Raises:
            Exception: If response code is not equal to set status code
        """
        response = self.call("/categories/_meta", method="GET", status=200)
        if raw == False:
            return self.marshall(MetaSchema(), response)
        else:
            return response


class AmbiverseNLU(__BaseClient):
    BASE_PATH = "entitylinking"

    def __init__(self, hostname: str, port: int = 80, path: str = None, protocol: str = "http"):
        """
        Args:
            hostname (str): Hostname
            port (int): Port
            path (str): Subpath of the endpoint
            protocol (str): Protocol to use (http|https)
        """
        path = urljoin(path, self.BASE_PATH).strip("/")
        super().__init__(hostname, port, path, protocol)

    def analyze(self, analyze_input: AnalyzeInput, raw: bool = False) -> Union[AnalyzeOutput, Dict]:
        """Analyze request
        Args:
            analyze_input (AnalyzeInput): Request object
            raw (bool): If True return raw dict
        Returns:
            dict: unprocessed result
            AnalyzeOutput: processed result
        Raises:
            Exception: If response code is not equal to set status code
        """
        if not isinstance(analyze_input, AnalyzeInput):
            raise Exception
        schema = AnalyzeInputSchema()
        analyze_input_dict = schema.dump(analyze_input)

        response = self.call("/analyze", method="POST", status=200, data=analyze_input_dict)
        if raw == False:
            return self.marshall(AnalyzeOutputSchema(), response)
        else:
            return response

    def meta(self, raw: bool = False) -> Union[Meta, Dict]:
        """Get meta information about the endpoint
        Args:
            raw (bool): If True return raw dict
        Returns:
            dict: unprocessed result
            Meta: processed result
        Raises:
            Exception: If response code is not equal to set status code
        """
        response = self.call("/analyze/_meta", method="GET", status=200)
        if raw == False:
            return self.marshall(MetaSchema(), response)
        else:
            return response
