from rest_framework.response import Response
from rest_framework import status


class BaseAPIView:
    def format_response(self, data="", message=None, success=True, status_code=status.HTTP_200_OK):
        formatted_response = {"message": message,
                              "data": data, "success": success}
        return Response(formatted_response, status=status_code)
