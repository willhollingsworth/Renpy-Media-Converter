image example1:
    "images/ball_000.jpg"
    function play_sound1
    pause 0.3
    "images/ball_001.jpg"
    pause 0.3
    "images/ball_002.jpg"
    function play_sound2
    pause 0.3
    "images/ball_003.jpg"
    pause 0.3
    "images/ball_004.jpg"
    pause 0.3
    repeat

label start:
    show example1
    return

init python:
    def play_sound1(trans, st, at):
        renpy.music.play("audio/test_tone_200.wav", channel="sound")
    def play_sound2(trans, st, at):
        renpy.music.play("audio/test_tone_300.wav", channel="sound")