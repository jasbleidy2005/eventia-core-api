from flask import Blueprint
from src.controllers.event_controller import EventController

event_bp = Blueprint('events', __name__, url_prefix='/api/events')
controller = EventController()

@event_bp.route('', methods=['POST'])
def create_event():
    return controller.create_event()

@event_bp.route('', methods=['GET'])
def get_all_events():
    return controller.get_all_events()

@event_bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
    return controller.get_event(event_id)

@event_bp.route('/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    return controller.update_event(event_id)

@event_bp.route('/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    return controller.delete_event(event_id)