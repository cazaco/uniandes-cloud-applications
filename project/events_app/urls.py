from django.urls import path

from . import views

app_name = 'events_app'

urlpatterns = [
    path(
        '',
        views.sign_in,
        name='login'
    ),
    path(
        'check_login',
        views.check_login,
        name='check_login'
    ),
    path(
        'sign_up',
        views.sign_up,
        name='sign_up'
    ),
    path(
        'check_sign_up',
        views.check_sign_up,
        name='check_sign_up'
    ),
    path(
        'log_out',
        views.log_out,
        name='log_out'
    ),
    path(
        'profile',
        views.profile,
        name='profile'
    ),
    path(
        'profile/create_event',
        views.create,
        name='create'
    ),
    path(
        'profile/check_created_event',
        views.check_created_event,
        name='check_created_event'
    ),
    path(
        'profile/edit_event/<int:event_id>',
        views.edit,
        name='edit'
    ),
    path(
        'profile/check_edited_event/<int:event_id>',
        views.check_edited_event,
        name='check_edited_event'
    ),
    path(
        'profile/delete_event/<int:event_id>',
        views.delete,
        name='delete'
    )
]
