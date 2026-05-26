#!/usr/bin/env python3

import typer

app = typer.Typer()

@app.command()
def add(time: str):
    """Add an alarm to database"""
    print(f"Adding alarm at {time}")

@app.command()
def foad(time: str):
    print(f"Adding foad at {time}")

app()