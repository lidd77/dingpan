import logging
import logging.handlers
import smtplib
import logging.config
from logging.handlers import RotatingFileHandler, SMTPHandler

from datetime import datetime


class SSLSMTPHandler(SMTPHandler):
    def emit(self, record):
        try:
            port = 465
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP_SSL(self.mailhost, port)
            msg = self.format(record)
            if self.username:
                smtp.login('yang.de.min@qq.com', 'pofcnsyjofoubdig')
            smtp.sendmail('yang.de.min@qq.com','yangdemin1990@163.com', "helolo")
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

def testLog():
  LOG_FORMAT = "%(asctime)s-%(levelname)s-%(filename)s:%(lineno)d  %(message)s"
  #FileNAME_FORMAT = "%Y%m%d-.log"
  filename1 = datetime.now().strftime("%Y%m%d-%H%M%S")+'.log'
  logging.basicConfig(filename=filename1, level=logging.INFO, format=LOG_FORMAT)

  # logging.debug("This is a debug log.")
  # logging.info("This is a info log.")
  # logging.warning("This is a warning log.")
  # logging.error("This is a error log.")
  # logging.critical("This is a critical log.")

# testLog()

def testLogMail():
  logger = logging.getLogger('test')
  logger.setLevel(logging.DEBUG)
  handler = logging.handlers.SMTPHandler(
    ('smtp.qq.com',587), 
    #('imap.163.com',993), 
    'yang.de.min@qq.com',
    ['yangdemin1990@163.com'], 
    'Python error test', 
    ('yang.de.min@qq.com','pofcnsyjofoubdig'))

  handler.setLevel(logging.DEBUG)

  logger.addHandler(handler)

  logger.isEnabledFor(logging.DEBUG)

  print(handler)

  #logger.debug("This is a debug log.")
  #logger.info("This is a info log.")
  #logger.warning("This is a warning log.")
  logger.error("This is a error log.")
  #logger.critical("This is a critical log.")

testLogMail()


def testLogMail2():
  logging.config.fileConfig("logging.conf")
  logger = logging.getLogger('test')
  logger.info('hello body ~')

# testLogMail2()


# Provide a class to allow SSL (Not TLS) connection for mail handlers by overloading the emit() method

'''
logger = logging.getLogger('')
# Create equivalent mail handler
handler = SSLSMTPHandler(mailhost=('smtp.qq.com', 465),
                           fromaddr='yang.de.min@qq.com',
                           toaddrs=['yangdemin1990@163.com'],
                           subject='yangdeminAAA',
                           credentials=('yang.de.min@qq.com','pofcnsyjofoubdig'))

# Set the email format
handler.setFormatter(logging.Formatter( "%(asctime)s" ))

# Only email errors, not warnings
handler.setLevel(logging.ERROR)
logger.addHandler(handler)
logger.isEnabledFor(logging.DEBUG)
logger.error("This is very important.AAAAAAAAAAAAAAAAA")
logger.error("This is very important.BBBBBBBBBBBBBBBB")
logger.error("This is very important.CCCCCCCCCCCCCCCCCCC")

logging.error("This is very important.AAAAAAAAAAAAAAAAA11111")
logging.error("This is very important.BBBBBBBBBBBBBBBB22222")
logging.error("This is very important.CCCCCCCCCCCCCCCCCCC333")
'''