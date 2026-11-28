import logging

import requests

from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class TipaxProvider:

    BASE_URL = 'https://omtestapi.tipax.ir/api/OM/v4/'

    def __init__(self, carrier):
        self.carrier = carrier.sudo()

    def request(self, method, path, payload=None):
        carrier = self.carrier

        if carrier.prod_environment:
            raise UserError(
                'Production is disabled in this sandbox build.'
            )

        if not carrier.tipax_api_key:
            raise UserError(
                'Configure the sandbox Bearer credential first.'
            )

        url = self.BASE_URL + path.lstrip('/')

        headers = {
            'Authorization': 'Bearer ' + carrier.tipax_api_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        _logger.info(
            'Tipax API Request | Method: %s | Endpoint: %s',
            method,
            path,
        )

        try:
            response = requests.request(
                method=method,
                url=url,
                json=payload,
                headers=headers,
                timeout=30,
                allow_redirects=False,
            )

        except requests.exceptions.Timeout:
            _logger.warning(
                'Tipax API timeout | Endpoint: %s',
                path,
            )

            raise UserError(
                'Tipax API request timed out. '
                'For registration, verify the remote order '
                'before retrying.'
            )

        except requests.exceptions.ConnectionError:
            _logger.warning(
                'Tipax API connection error | Endpoint: %s',
                path,
            )

            raise UserError(
                'Could not connect to Tipax API. '
                'For registration, verify the remote order '
                'before retrying.'
            )

        except requests.exceptions.RequestException:
            _logger.warning(
                'Tipax API request failed | Endpoint: %s',
                path,
            )

            raise UserError(
                'Tipax network error. '
                'For registration, verify the remote order '
                'before retrying.'
            )

        _logger.info(
            'Tipax API Response | Endpoint: %s | HTTP Status: %s',
            path,
            response.status_code,
        )

        if not 200 <= response.status_code < 300:
            _logger.warning(
                'Tipax HTTP error | Endpoint: %s | Status: %s',
                path,
                response.status_code,
            )

            raise UserError(
                'Tipax HTTP %s\n\nResponse:\n%s'
                % (
                    response.status_code,
                    response.text[:2000],
                )
            )

        try:
            result = response.json()

        except ValueError:
            # Some endpoints may return plain text or an empty body.
            return response.text

        if isinstance(result, dict):

            if (
                result.get('isSuccess') is False
                or result.get('success') is False
            ):
                message = (
                    result.get('message')
                    or result.get('errorMessage')
                    or result.get('errors')
                    or result.get('error')
                    or 'Unknown Tipax API error.'
                )

                _logger.warning(
                    'Tipax rejected request | Endpoint: %s',
                    path,
                )

                raise UserError(
                    'Tipax rejected the request.\n\n'
                    'Response:\n%s' % str(message)[:2000]
                )

            return result.get('data', result)

        return result