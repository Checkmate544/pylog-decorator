import logging
import time
from functools import wraps
from typing import Callable, Optional, Dict, Any, Union


class LoggerDecorator:
    def __init__(self, logger_name: str = '__main__',
                 formatter_str: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                 log_file: Optional[str] = None):
        # 初始化logger
        self.logger = logging.getLogger(logger_name)

        # 创建格式化器
        formatter = logging.Formatter(formatter_str)

        # 控制台处理器
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        # 可选的文件处理器
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        # 日志级别映射
        self.LOG_LEVELS = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }

    def log_execution(self, level: str = 'DEBUG',
                      log_args: bool = False,
                      log_result: bool = False,
                      exception_handling: str = 'log') -> Callable:
        """
        记录函数执行的装饰器
        :param level: 日志级别
        :param log_args: 是否记录参数
        :param log_result: 是否记录返回结果
        :param exception_handling: 异常处理方式 ('log', 'raise', 'both')
        :return: 装饰后的函数
        """

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # 获取日志级别
                log_level = self.LOG_LEVELS.get(level.upper(), logging.DEBUG)
                self.logger.setLevel(log_level)

                # 获取函数信息
                func_name = func.__name__

                # 记录函数参数
                args_str = ""
                if log_args and (args or kwargs):
                    args_str = f", args: {args}, kwargs: {kwargs}"

                # 记录开始执行
                start_time = time.time()
                start_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
                self.logger.log(log_level, f"Function '{func_name}' started at {start_time_str}{args_str}")

                try:
                    # 执行函数
                    result = func(*args, **kwargs)

                    # 记录执行结束
                    end_time = time.time()
                    end_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))
                    execution_time = end_time - start_time

                    # 构建结果日志
                    result_str = ""
                    if log_result:
                        result_str = f", result: {result}"

                    self.logger.log(
                        log_level,
                        f"Function '{func_name}' completed at {end_time_str} (took {execution_time:.4f}s){result_str}"
                    )

                    return result

                except Exception as e:
                    # 异常处理
                    error_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                    error_msg = f"Function '{func_name}' failed at {error_time}: {e.__class__.__name__}: {str(e)}"

                    self.logger.error(error_msg)

                    if exception_handling in ('raise', 'both'):
                        raise

            return wrapper

        return decorator