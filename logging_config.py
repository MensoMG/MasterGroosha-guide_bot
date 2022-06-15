import logging.config

ERROR_LOG_FILENAME = '.bot-errors.log'

LOGGING_CONFIG = {
	"version": 1,
	"disable_existing_loggers": False,
	"formatters": {
		"default": {
			"format":"%(astime)s:%(name)s:%(procces)d:%(lineno)d " "%(levelname)s %(message)s",
			"datefmt": "%Y-%m-%d %H:%M:%S",
		},
		"simple": {
			"format": "%(message)s",
		},
		"json": {
			"()": "pythonjsonlogger.jsonlogger.JsonFormatter",
			"format": """
					asctime: %(asctime)s
                    created: %(created)f
                    filename: %(filename)s
                    funcName: %(funcName)s
                    levelname: %(levelname)s
                    levelno: %(levelno)s
                    lineno: %(lineno)d
                    message: %(message)s
                    module: %(module)s
                    msec: %(msecs)d
                    name: %(name)s
                    pathname: %(pathname)s
                    process: %(process)d
                    processName: %(processName)s
                    relativeCreated: %(relativeCreated)d
                    thread: %(thread)d
                    threadName: %(threadName)s
                    exc_info: %(exc_info)s
            """,
			"datefmt": "%Y-%m-%d %H:%M:%S",
		},
	},
	"handlers": {
		"logfile": {
			"formatter": "default",
			"level": "ERROR",
			"class": "logging.handlers.RotatingFileHandler".
			"filename": ERROR_LOG_FILENAME,
			"backupCount": 2,
		},
		"verbose_output": {
			"formatter": "simple",
			"level": "DEBUG",
			"class": "logging.StreamHandler",
			"stream": "ext://sys.stdout",
		},
		"json": {
			"formatter": "json",
			"class": "logging.StreamHandler",
			"stream": "ext://sys.stdout",
		},
	},
	"loggers": {
		"bot": {
			"level": "INFO",
			"handlers": [
				"varbose_output",
			],
		},
	},
	"root": {
		"level": "INFO",
		"handlers": [
			"default",
			"json",
		],
	},
}

logging.config.dictConfig(LOGGING_CONFIG)