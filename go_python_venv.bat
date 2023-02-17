@echo off
title python_venv
start/b Scripts\activate.bat

pyinstaller -F --icon=kakaoview_autosystem.ico kakaoview_autosystem_V4.py