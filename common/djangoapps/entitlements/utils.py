"""
Utility methods for the entitlement application.
"""

import logging
import analytics
from eventtracking import tracker
from six import text_type

from django.conf import settings
from django.utils import timezone

from course_modes.models import CourseMode
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from track import contexts


log = logging.getLogger("common.entitlements.utils")


def is_course_run_entitlement_fulfillable(course_run_key, entitlement, compare_date=timezone.now()):
    """
    Checks that the current run meets the following criteria for an entitlement

    1) Is currently running or start in the future
    2) A User can enroll in
    3) A User can upgrade to the entitlement mode

    Arguments:
        course_run_key (CourseKey): The id of the Course run that is being checked.
        entitlement: The Entitlement that we are checking against.
        compare_date: The date and time that we are comparing against.  Defaults to timezone.now()

    Returns:
        bool: True if the Course Run is fullfillable for the CourseEntitlement.
    """
    try:
        course_overview = CourseOverview.get_from_id(course_run_key)
    except CourseOverview.DoesNotExist:
        log.error(('There is no CourseOverview entry available for {course_run_id}, '
                   'course run cannot be applied to entitlement').format(
            course_run_id=str(course_run_key)
        ))
        return False

    # Verify that the course is still running
    run_start = course_overview.start
    run_end = course_overview.end
    is_running = run_start and (not run_end or (run_end and (run_end > compare_date)))

    # Verify that the course run can currently be enrolled
    enrollment_start = course_overview.enrollment_start
    enrollment_end = course_overview.enrollment_end
    can_enroll = (
        (not enrollment_start or enrollment_start < compare_date)
        and (not enrollment_end or enrollment_end > compare_date)
    )

    # Ensure the course run is upgradeable and the mode matches the entitlement's mode
    unexpired_paid_modes = [mode.slug for mode in CourseMode.paid_modes_for_course(course_run_key)]
    can_upgrade = unexpired_paid_modes and entitlement.mode in unexpired_paid_modes

    return is_running and can_upgrade and can_enroll

def emit_entitlement_session_event(user_id, session_action, course_run_key):
    """
    Tracks a user's entitlement session selection (switch or first time selection)

    Arguments:
        user_id (str): the ID of the user selecting or switching sessions
        session_action (str): action taken by user to be tracked
        course_run_key (CourseKey): identifier for the course run, aka session, the user is selecting
    """
    event_name = 'edx.course.entitlement.session.' + session_action
    if hasattr(settings, 'LMS_SEGMENT_KEY') and settings.LMS_SEGMENT_KEY:
        analytics.track(user_id, event_name, {
            'category': 'user-engagement',
            'label': CourseOverview.get_from_id(course_run_key).display_name,
            'display': str(course_run_key),
        })
