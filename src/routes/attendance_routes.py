from flask import Blueprint
from src.controllers.attendance_controller import AttendanceController

attendance_bp = Blueprint('attendance', __name__, url_prefix='/api/attendance')
controller = AttendanceController()

@attendance_bp.route('', methods=['POST'])
def register_attendance():
    return controller.register_attendance()

@attendance_bp.route('/event/<int:event_id>/participants', methods=['GET'])
def get_event_participants(event_id):
    return controller.get_event_participants(event_id)

@attendance_bp.route('/participant/<int:participant_id>/events', methods=['GET'])
def get_participant_events(participant_id):
    return controller.get_participant_events(participant_id)

@attendance_bp.route('/event/<int:event_id>/statistics', methods=['GET'])
def get_event_statistics(event_id):
    return controller.get_event_statistics(event_id)

@attendance_bp.route('/event/<int:event_id>/participant/<int:participant_id>', methods=['DELETE'])
def cancel_attendance(event_id, participant_id):
    return controller.cancel_attendance(event_id, participant_id)