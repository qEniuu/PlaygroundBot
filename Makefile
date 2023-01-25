test:
	python -c "import playground_bot; import logging; FORMAT = '%(levelname)s %(name)s %(asctime)-15s %(filename)s:%(lineno)d %(message)s'; logging.basicConfig(format=FORMAT); logging.getLogger().setLevel(logging.DEBUG); print(playground_bot.brainfuck.interpret('++++++++++++++++++++++++++++++++++++++++++++[+>]<...[>+.]', '', 100))"  C-c C-c

run:
	python -c "import playground_bot; print(playground_bot.brainfuck.interpret('++++++++++++++++++++++++++++++++++++++++++++...', '', 1000))"
