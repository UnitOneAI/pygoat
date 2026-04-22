from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views import View
import json

from .main import Log


class LogFunctionTarget(View):
    def dispatch(self, request, *args, **kwargs):
        self.L = Log(request)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        self.L.info("GET request")
        csrf_token = get_token(request)
        return JsonResponse({"message":"normal get request", "method":"get", "csrf_token": csrf_token}, status=200)
    
    def post(self, request):
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                username = data.get('username')
                password = data.get('password')
            else:
                username = request.POST['username']
                password = request.POST['password']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({"message":"Invalid request data", "method":"post"}, status=400)
        
        self.L.info(f"POST request with username {username} and password {password}")
        if username == "admin" and password == "admin":
            return JsonResponse({"message":"Loged in successfully", "method":"post"}, status=200)
        return JsonResponse({"message":"Invalid credentials", "method":"post"}, status=401)
    
    def put(self, request):
        self.L.info("PUT request")
        return JsonResponse({"message":"success", "method":"put"}, status=200)
    
    def delete(self, request):
        if request.user.is_authenticated:
            return JsonResponse({"message":"User is authenticated", "method":"delete"}, status=200)
        self.L.error("DELETE request")
        return JsonResponse({"message":"permission denied", "method":"delete"}, status=200)
    
    def patch(self, request):
        self.L.info("PATCH request")
        return JsonResponse({"message":"success", "method":"patch"}, status=200)
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        if request.method == "UPDATE":
            return JsonResponse({"message":"success", "method":"update"}, status=200)
        return JsonResponse({"message":"method not allowed"}, status=403)

log_function_target = LogFunctionTarget.as_view()