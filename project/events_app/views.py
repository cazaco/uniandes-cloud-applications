from datetime import datetime
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from . import constants
from . import models


logging.basicConfig(
    format='%(levelname)s:%(message)s',
    level=logging.DEBUG
)


def sign_in(request):
    logging.info(""" Rendering login template. """)

    return render(
        request,
        'events_app/login.html',
        {
            'message': request.session.pop('message', None)
        }
    )


def check_login(request):
    args = request.POST
    email, password = args['email'], args['password']

    logging.debug("""
        Email: '{email}'
        Password: '{password}'
    """.format(**args))

    try:
        user = authenticate(
            username=email,
            password=password
        )

        if user is not None:
            logging.info(user)
            login(request, user)

            message = """
                User '{username}' has been signed in successfully.
            """.format(username=email)

            logging.info(message)

            request.session['message'] = message

            return redirect('events_app:profile')
        else:
            message = """
                Invalid password for '{email}'.
            """.format(**args)

            request.session['message'] = message

            return redirect('events_app:login')
    except Exception as exception:
        message = """
            There's not exist a registered user with email '{email}'.
            Please, sign up first.
        """.format(**args)

        logging.error(str(exception))

        request.session['message'] = message

        return redirect('events_app:login')


def sign_up(request):
    return render(
        request,
        'events_app/sign_up.html',
        {
            'message': request.session.pop('message', None)
        }
    )


def check_sign_up(request):
    args = request.POST
    email, password = args['email'], args['password']

    logging.debug("""
        Email: '{email}'
        Password: '{password}'
    """.format(**args))

    result_set = User.objects.filter(username=email)

    if result_set.count() == 0:
        new_user = User.objects.create_user(
            username=email,
            password=password
        )

        new_user.save()

        message = """
            A new user with email '{email}' was successfully created.
        """.format(email=email)

        logging.info(message)

        request.session['message'] = message

        return redirect('events_app:login')
    else:
        message = """
            The email '{email}' is being used by another user.
            Please try a new email.
        """.format(email=email)

        logging.info(message)

        request.session['message'] = message

        return redirect('events_app:sign_up')


def log_out(request):
    message = """
        You were successfully logged out.
    """

    logging.info(message)
    logout(request)
    request.session['message'] = message

    return redirect('events_app:login')


@login_required(login_url='/events_app/')
def profile(request):
    events = (
        models
        .Event
        .objects
        .filter(user=request.user)
        .order_by('-created_at')
    )

    return render(
        request,
        'events_app/profile.html',
        {
            'events': events,
            'message': request.session.pop('message', None)
        }
    )


@login_required(login_url='/events_app/')
def create(request):
    return render(request, 'events_app/create.html')


@login_required(login_url='/events_app/')
def check_created_event(request):
    args = request.POST

    logging.info("""
        name: '{name}'
        category: '{category}'
        place: '{place}'
        address: '{address}'
        start_date: '{start_date}'
        end_date: '{end_date}'
        is_virtual: '{is_virtual}'
    """.format(**args))

    name = args['name']
    category = args['category']
    place = args['place']
    address = args['address']

    start_date = datetime.strptime(
        args['start_date'],
        constants.DATE_FORMAT
    )

    end_date = datetime.strptime(
        args['end_date'],
        constants.DATE_FORMAT
    )

    created_at = datetime.utcnow()

    is_virtual = int(args['is_virtual']) == 1

    user = request.user

    event = models.Event(
        name=name,
        category=category,
        place=place,
        address=address,
        start_date=start_date,
        end_date=end_date,
        is_virtual=is_virtual,
        user=user,
        created_at=created_at
    )

    event.save()

    message = """
        The event '{name}' was successfully created.
    """.format(name=name)

    logging.info(message)

    request.session['message'] = message

    return redirect('events_app:profile')


@login_required(login_url='/events_app/')
def edit(request, event_id):
    event = models.Event.objects.get(id=event_id)

    logging.info("""
        Rendering Edit Event View
        The event_id {event_id} is going to be edited.
    """.format(event_id=event_id))

    return render(
        request,
        'events_app/edit.html',
        {
            'event': event,
            'start_date': event.start_date.strftime(constants.DATE_FORMAT),
            'end_date': event.end_date.strftime(constants.DATE_FORMAT)
        }
    )


@login_required(login_url='/events_app/')
def check_edited_event(request, event_id):
    args = request.POST

    logging.info("""
        name: '{name}'
        category: '{category}'
        place: '{place}'
        address: '{address}'
        start_date: '{start_date}'
        end_date: '{end_date}'
        is_virtual: '{is_virtual}'
    """.format(**args))

    event = models.Event.objects.get(id=event_id)

    event.name = args['name']
    event.category = args['category']
    event.place = args['place']
    event.address = args['address']

    event.start_date = datetime.strptime(
        args['start_date'],
        constants.DATE_FORMAT
    )

    event.end_date = datetime.strptime(
        args['end_date'],
        constants.DATE_FORMAT
    )

    event.is_virtual = int(args['is_virtual']) == 1

    event.save()

    message = """
        The event '{name}' has been successfully updated.
    """.format(name=event.name)

    logging.info(message)

    request.session['message'] = message

    return redirect('events_app:profile')


@login_required(login_url='/events_app/')
def delete(request, event_id):
    event = models.Event.objects.get(id=event_id)

    message = """
        The event '{name}' has been deleted successfully.
    """.format(name=event.name)

    logging.info(message)

    event.delete()

    request.session['message'] = message

    return redirect('events_app:profile')
