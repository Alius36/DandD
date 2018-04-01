# coding: utf-8
import logging

from pyramid.httpexceptions import HTTPOk, HTTPNotAcceptable, HTTPInternalServerError, HTTPInsufficientStorage, \
    HTTPConflict, HTTPBadRequest
from pyramid.view import view_config

from DandD.controllers.manual_controller import ManualController

logger = logging.getLogger(__name__)


class Manual:
    def __init__(self, request):
        self.request = request
        self.bad_request = 400
        self.conflict_request = 409
        self.internal_server_error = 500
        self.memory_error = 507
        self.not_acceptable_request = 406
        self.success_request = 200

    @view_config(route_name='upload', renderer='json', request_method='POST', permission='play')
    def upload_manuals(self):
        file_upload = self.request.params.get('file', None)
        md5 = self.request.params.get('md5', None)

        if file_upload is not None:
            result = ManualController.upload(self.request, file_upload, md5)
            if result["code"] == self.success_request:
                return HTTPOk(body=result["message"])
            elif result["code"] == self.not_acceptable_request:
                return HTTPNotAcceptable(body=result["message"])
            elif result["code"] == self.conflict_request:
                return HTTPConflict(body=result["message"])
            elif result["code"] == self.internal_server_error:
                return HTTPInternalServerError(body=result["message"])
            elif result["code"] == self.memory_error:
                return HTTPInsufficientStorage(body=result["message"])
            else:
                return HTTPInternalServerError(body="Stiamo riscontrando un'anomalia a livello di sistema. Ci scusiamo "
                                                    "per l'inconveniente!")
        else:
            return HTTPBadRequest(body="Selezionare un file.")
