from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from .models import Game


def home(request):
    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip()
        option = request.POST.get('option')
        room_code = (request.POST.get('room_code') or '').strip()

        if not username:
            messages.error(request, 'Please enter a username.')
            return redirect('/')

        if not room_code:
            messages.error(request, 'Please enter a room code.')
            return redirect('/')

        if option == '1':
            game = Game.objects.filter(room_code=room_code).first()
            if game is None:
                messages.error(request, 'Room code not found.')
                return redirect('/')

            if game.is_over:
                messages.error(request, 'Game is over.')
                return redirect('/')

            if game.game_opponent and game.game_opponent != username:
                messages.error(request, 'Room already has two players.')
                return redirect('/')

            game.game_opponent = username
            game.current_turn = game.game_creator
            game.save()
            return redirect(f'/play/{room_code}/?username={username}')

        game = Game.objects.filter(room_code=room_code).first()
        if game:
            messages.error(request, 'Room code already exists. Use join mode.')
            return redirect('/')

        try:
            Game.objects.create(
                room_code=room_code,
                game_creator=username,
                current_turn=username,
            )
        except IntegrityError:
            messages.error(request, 'Room code already exists. Use join mode.')
            return redirect('/')

        return redirect(f'/play/{room_code}/?username={username}')

    return render(request, 'home.html')


def play(request, room_code):
    username = request.GET.get('username', '')
    game = Game.objects.filter(room_code=room_code).first()

    if game is None:
        messages.error(request, 'Room not found.')
        return redirect('/')

    if username and username not in {game.game_creator, game.game_opponent or ''}:
        messages.error(request, 'You must join through the home page.')
        return redirect('/')

    context = {
        'room_code': room_code,
        'username': username,
        'game_creator': game.game_creator,
        'game_opponent': game.game_opponent or 'Waiting for opponent...',
        'board': game.board,
        'is_over': game.is_over,
        'winner': game.winner,
    }
    return render(request, 'play.html', context)
