from django.http import JsonResponse
from .models import TransferEvent

def transfer_history(request, token_id):
    # Query all transfer events for the token_id
    events = TransferEvent.objects.filter(token_id=token_id)

    # Check if any transfer events were found
    if not events.exists():
        return JsonResponse({'error': 'No events found'}, status=404)
    
    # Structure transfer events data in json format
    data = [{
        'token_id': event.token_id,
        'from_address': event.from_address,
        'to_address': event.to_address,
        'transaction_hash': event.transaction_hash,
        'block_number': event.block_number
    } for event in events]

    # Return transfer events data as a json response
    return JsonResponse({'events': data}, status=200)
