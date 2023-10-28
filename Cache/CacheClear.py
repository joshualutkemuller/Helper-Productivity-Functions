import os
import shutil
import time
import math

# Constraints
cache_directory = r"C:\Windows\Prefetch"
temp_directory = r"C:\Windows\Temp"
user_temp_directory = r"C:\Users\user_name\AppData\Local\Temp"

def calculate_time(func):
    """
    Decorator to calculate duration taken by any function
    """
    def innerl(*args, **kwargs):

        #storing time before function execution
        begin = time.time()

        func(*args, **kwargs)

        # storing time after function
        end = time.time()
        print("Total time taken in :", func.__name__,end-begin)

    return innerl

#@calculate_time
def attempt_function(func, *args, max_attempts=5, **kwargs):
    """
    Attempt to run a function and allow it to fail up to max attempt times.
    Used extensively in situtations where scraping is neccsary or time complexity is heavily dependent on size

    Parameters:
    - func: The function to execute.
    - *args: Arguments to pass to function.
    - max_attempts: The maximum number of times to retry the function.
    - **kwargs: Keyword arguments to pass to the function.

    Returns:
    - The result of the function if successful.
    """
    print(f'Running the following function: {func}')

    for attempt in range(1, max_attempts+1):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f'Attempt {attempt} failed: {str(e)}')
            if attempt == max_attempts:
                print(f'{func} failed to complete, check code section')
                raise # If this was the last attempt, re-raise the exception to crash the pgoram, will output the exception that is caught

def clear_directory(directory_path) -> str:

    try: 
        for file in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                print(f'Skipped: {file_path} (Not a file or directory)')
    except Exception as e:
        print(f'Error clearing {directory_path}: {e}')

def main():
    print(f'Cleaning cache: {cache_directory}')
    attempt_function(clear_directory,cache_directory)

    print(f'Cleaning cache: {temp_directory}')
    attempt_function(clear_directory,temp_directory)

    print(f'Cleaning user temp: {user_temp_directory}')
    attempt_function(clear_directory,user_temp_directory)

if __name__ == "__main__":
    main()
