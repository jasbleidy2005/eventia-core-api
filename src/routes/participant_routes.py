from flask import Blueprint
from src.controllers.participant_controller import ParticipantController

participant_bp = Blueprint('participants', __name__, url_prefix='/api/participants')
controller = ParticipantController()

@participant_bp.route('', methods=['POST'])
def create_participant():
    return controller.create_participant()

@participant_bp.route('', methods=['GET'])
def get_all_participants():
    return controller.get_all_participants()

@participant_bp.route('/<int:participant_id>', methods=['GET'])
def get_participant(participant_id):
    return controller.get_participant(participant_id)

@participant_bp.route('/<int:participant_id>', methods=['PUT'])
def update_participant(participant_id):
    return controller.update_participant(participant_id)

@participant_bp.route('/<int:participant_id>', methods=['DELETE'])
def delete_participant(participant_id):
    return controller.delete_participant(participant_id)