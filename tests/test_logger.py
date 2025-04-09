from pylog_decorator.logger import LoggerDecorator

# 创建日志装饰器实例
logger_decorator = LoggerDecorator(logger_name='my_app', log_file='app.log')

# 基本用法
@logger_decorator.log_execution(level='INFO')
def calculate_sum(a, b):
    return a + b

# 记录参数和结果
@logger_decorator.log_execution(level='DEBUG', log_args=True, log_result=True)
def multiply(a, b):
    return a * b

# 异常处理 - 记录但不引发
@logger_decorator.log_execution(level='ERROR', exception_handling='log')
def divide(a, b):
    return a / b

# 测试
calculate_sum(5, 10)
multiply(4, 8)
try:
    divide(10, 0)  # 这里不会抛出异常
except:
    pass  # 不需要处理

# 异常处理 - 记录并引发
@logger_decorator.log_execution(level='ERROR', exception_handling='both')
def risky_operation():
    raise ValueError("Something went wrong")

try:
    risky_operation()  # 这里会抛出异常
except ValueError as e:
    print(f"Caught exception: {e}")