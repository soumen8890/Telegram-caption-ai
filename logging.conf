   [loggers]
   keys=root,bot

   [handlers]
   keys=consoleHandler,fileHandler

   [formatters]
   keys=simpleFormatter

   [logger_root]
   level=INFO
   handlers=consoleHandler

   [logger_bot]
   level=DEBUG
   handlers=fileHandler
   qualname=bot
   propagate=0

   [handler_consoleHandler]
   class=StreamHandler
   level=INFO
   formatter=simpleFormatter
   args=(sys.stdout,)

   [handler_fileHandler]
   class=FileHandler
   level=DEBUG
   formatter=simpleFormatter
   args=('bot.log', 'a')

   [formatter_simpleFormatter]
   format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
   datefmt=%Y-%m-%d %H:%M:%S
   
