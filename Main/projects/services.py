from .models import Project
from .constants import SLA_FLOW


def assign_project(project, manager):
    project.manager = manager
    project.status = 'assigned'
    project.save()


def add_associate(project, associate):
    project.associates.add(associate)


def update_status(project, new_status, user):
    current_status = project.status

    # check valid transition
    if new_status not in SLA_FLOW.get(current_status, []):
        raise Exception("Invalid status transition")

    # role-based control
    if user.role == 'associate':
        if new_status not in ['in_progress', 'review']:
            raise Exception("Associate cannot set this status")

    if user.role == 'manager':
        if new_status == 'closed':
            project.status = 'closed'
            project.save()
            return

    project.status = new_status
    project.save()