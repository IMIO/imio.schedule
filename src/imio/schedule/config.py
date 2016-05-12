# -*- coding: utf-8 -*-

# task status
CREATION = 'schedule_task_created'
STARTED = 'schedule_task_started'
DONE = 'schedule_task_done'

states_by_status = {
    CREATION: [
        'created',
        'to_assign'
    ],
    STARTED: [
        'to_do',
        'in_progress',
        'realized'
    ],
    DONE: [
        'closed'
    ],
}

status_by_state = {
    'created': CREATION,
    'to_assign': CREATION,
    'to_do': STARTED,
    'in_progress': STARTED,
    'realized': STARTED,
    'closed': DONE
}
