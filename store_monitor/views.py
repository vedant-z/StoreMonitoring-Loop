from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from store_monitor.models import StoreReport
from .report_generator import generate_report

@csrf_exempt
@require_POST
def trigger_report(request):
    # Trigger report generation
    report_id = generate_report()
    return JsonResponse({'report_id': report_id})

def get_report(request, report_id):
    # Check if the report is complete
    try:
        report = StoreReport.objects.get(report_id=report_id)
        return JsonResponse({'status': 'Complete', 'report': report.data})
    except StoreReport.DoesNotExist:
        return JsonResponse({'status': 'Running'})