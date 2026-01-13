import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .services.api_client import APIClient


@csrf_exempt
@require_http_methods(["GET"])
def fetch_data(request):
    #candidate_id = "candidate-faheem-i7hr" #request.headers.get("X-Candidate-ID", "candidate-faheem-i7hr")
    batch = request.GET.get("batch", "1")

    api = APIClient()
    data, error = api.fetch_data(batch)

    if error:
        return JsonResponse({
            "success": False,
            "error": error
        }, status=500)

    return JsonResponse({
    "success": True,
    "data": data.get("records", [])
})


@csrf_exempt
@require_http_methods(["POST"])
def submit_data(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    candidate_name = payload.get("candidate_name")
    batch_id = payload.get("batch_id")
    cleaned_items = payload.get("cleaned_items")

    if not candidate_name or not batch_id or not cleaned_items:
        return JsonResponse({
            "error": "candidate_name, batch_id and cleaned_items are required"
        }, status=400)

    api = APIClient()
    result, error = api.submit_data(candidate_name, batch_id, cleaned_items)

    if error:
        return JsonResponse({
            "success": False,
            "error": error
        }, status=500)

    return JsonResponse({
        "success": True,
        "result": result
    })
