import logging.config
import logging
import argparse
import sys
import os


class Greetings(object):

    def __init__(self, args):
        self.args = args
        self.create_logger("logger_test.properties")
        self.logger.info("ProgressInfo:0.0%")

    def run(self):
        try:
            trg = '%s/../../../output/%s/greetings.xml' % (os.path.dirname(
                os.path.abspath(__file__)), self.args.execution_id)
            file = open(trg, "w")
            file.write("<greeting>Hello, %s</greeting>" % self.args.theName)
            file.close()

            ret = 0
            self.logger.info("ProgressInfo:100%")
        except:
            ret = -1
            self.logger.critical("Error occurred during processing.")

        return ret

    def create_logger(self, logger_config_file):
        defaults = {}

        logging.config.fileConfig(str(logger_config_file), defaults=defaults)

        self.logger = logging.getLogger("main.create_logger")

        self.logger.debug("Logger initialized with file " + str(logger_config_file))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--theName", nargs='?', default="Alessio", help="The Name.")
    parser.add_argument("-w", "--workdir", nargs='?', default="", help="Remote process sandbox working directory.")
    parser.add_argument("-e", "--execution_id", nargs='?', default="", help="Remote process Unique Execution Id.")
    cmdargs = parser.parse_args()

    greeting = Greetings(cmdargs)
    return_code = greeting.run()
    sys.exit(return_code)
