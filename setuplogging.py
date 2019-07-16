# noinspection PyUnresolvedReferences
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-7s [%(name)-8s] %(filename)s:%(lineno)d %(funcName)s() %(message)s',
    level=logging.DEBUG,
)

logging.getLogger('protocol').setLevel(logging.INFO)
