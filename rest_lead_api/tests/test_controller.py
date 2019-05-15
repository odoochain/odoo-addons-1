# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#   oe -Q rest_lead_api -c click -d click_prod


from odoo.http import controllers_per_module

from .common import CommonCase
from ..controllers.main import BaseRestPrivateApiController, \
    BaseRestPublicApiController


class TestController(CommonCase):

    def _check_default_routes(self, controller_cls, auth, root_path):
        for method_name in ('get', 'modify', 'update', 'delete'):
            method = getattr(controller_cls, method_name, None)
            self.assertIsNotNone(
                method,
                'Method %s is not declared on the controller %s' % (
                    method_name,
                    controller_cls
                ))
            routing = getattr(method, 'routing', None)
            # check that routes are defiend on method
            self.assertIsNotNone(
                routing,
                'No route defeined on method %s of controller %s' % (
                    method_name,
                    controller_cls
                )
            )
            # check the auth defined
            self.assertEqual(
                routing.get('auth'),
                auth,
                'Wrong auth defined on method %s' % method_name
            )
            # ensure that the route startswith the right root..
            routes = routing.get('routes', [])
            self.assertTrue(routes)
            for route in routes:
                self.assertTrue(
                    route.startswith(root_path),
                    'Route %s should start with %s' % (route, root_path)
                )

    def test_controller_registry(self):
        # at the end of the start process, our tow controllers must into the
        # controller registered
        controllers = controllers_per_module['rest_lead_api']
        self.assertEqual(len(controllers), 2)

        self.assertIn(
            ('odoo.addons.rest_lead_api.controllers.main.'
             'BaseRestPrivateApiController',
             BaseRestPrivateApiController),
            controllers
        )
        self.assertIn(
            ('odoo.addons.rest_lead_api.controllers.main.'
             'BaseRestPublicApiController',
             BaseRestPublicApiController),
            controllers
        )

    def test_controller_routes(self):
        # check that the generic routes are defined with the right url and auth
        self._check_default_routes(
            BaseRestPrivateApiController, auth="api_key",
            root_path="/v1/private/"
        )
