import atexit
import logging
from logging.handlers import MemoryHandler
import os


class BufferedLogger:
    def __init__(self, output_dir="", log_filename="log.log", **kwargs):
        self.buffer = kwargs.get("buffer", 10)

        logger = logging.getLogger("log")
        logger.propagate = False

        if "log_to_file" in kwargs.keys() or "log_to_stream" in kwargs.keys():
            if kwargs["log_to_file"] or kwargs["log_to_stream"]:
                log_filename = os.path.join(output_dir, log_filename)
                logger.setLevel(logging.INFO)

                if kwargs["log_to_file"]:
                    to_buffer = MemoryHandler(100, flushOnClose=True)
                    logger.addHandler(to_buffer)

                if kwargs["log_to_stream"]:
                    to_stdout = logging.StreamHandler()
                    format_stdout = logging.Formatter(
                        "%(asctime)s %(message)s", datefmt="%Y-%m-%d %I:%M:%S %p"
                    )
                    to_stdout.setFormatter(format_stdout)
                    logger.addHandler(to_stdout)

        self.logger = logger
        self.log_file_name = log_filename
        self.level = 60
        self.date_format = "%Y-%m-%d %I:%M:%S %p"
        atexit.register(self.cleanup)

    def __call__(self, msg):
        self.logger.log(self.level, msg)
        if self.log_file_name and any(
                [True for x in self.logger.handlers if isinstance(x, MemoryHandler)]
        ):
            for x in self.logger.handlers:
                if isinstance(x, MemoryHandler):

                    if len(x.buffer) > self.buffer:

                        try:
                            to_file = logging.FileHandler(self.log_file_name, mode="a")
                            format_file = logging.Formatter(
                                "%(asctime)s %(message)s",
                                datefmt=self.date_format,
                            )
                            to_file.setFormatter(format_file)

                            x.setTarget(to_file)
                            x.flush()
                            x.setTarget(None)
                            to_file.close()
                        except:
                            pass

    def cleanup(self):
        if self.log_file_name and any(
                [True for x in self.logger.handlers if isinstance(x, MemoryHandler)]
        ):
            for x in self.logger.handlers:
                if isinstance(x, MemoryHandler):
                    try:
                        to_file = logging.FileHandler(self.log_file_name, mode="a")
                        format_file = logging.Formatter(
                            "%(asctime)s %(message)s",
                            datefmt=self.date_format,
                        )
                        to_file.setFormatter(format_file)

                        x.setTarget(to_file)
                        x.flush()
                        x.setTarget(None)
                        to_file.close()
                    except:
                        pass

        # close all the logging handlers
        log_handlers = self.logger.handlers[:]
        for handler in log_handlers:
            handler.close()
            self.logger.removeHandler(handler)


if __name__ == "__main__":
    pass
