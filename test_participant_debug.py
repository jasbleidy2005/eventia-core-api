from src.app import create_app
import json

app = create_app()
app.config['TESTING'] = True

with app.test_client() as client:
    participant_data = {
        'name': 'Juan Pérez',
        'email': 'juan@example.com',
        'phone': '1234567890'
    }
    
    response = client.post(
        '/api/participants',
        data=json.dumps(participant_data),
        content_type='application/json'
    )
    
    print("\n" + "="*60)
    print("STATUS CODE:", response.status_code)
    print("="*60)
    print("RESPONSE:")
    print(response.data.decode('utf-8'))
    print("="*60)
    
    # Probar directamente el servicio
    print("\nProbando el servicio directamente...")
    try:
        from src.services.participant_service import ParticipantService
        from src.models.participant import Participant
        
        service = ParticipantService()
        participant = Participant(
            name='Test',
            email='test@example.com',
            phone='123456'
        )
        result = service.create_participant(participant)
        print("✅ Servicio funciona!")
        print(f"Resultado: {result.to_dict()}")
    except Exception as e:
        print(f"❌ Error en servicio: {e}")
        import traceback
        traceback.print_exc()