# File Guard: Preserve The Content Of Files and Directories

Protect the content of your files and directories in a certain scope.
In that scope, you can change the contents of the file/directory as you wish.
After the scope has ended, the original contents of the file(s) and/or
directory(ies) will be restored. The "scope" can either be a `with` block or a
function/method.

Below is an example of guarding the contents of the `allure.txt` file.
Inside the `with guard('allure.txt')` block, the content of the file is
changed. However, after its scope ends, the previous content of the file is
restored:

```python
>>> from fileguard import guard
>>> with open('allure.txt', 'r') as f:
        print(f.read())

The allure of breaking the law
Was always too much for me to ever ignore
>>> with guard('allure.txt'):
        with open('allure.txt', 'w') as f:
           f.write('Still Dre Day')

        with open('allure.txt', 'r') as f:
            print(f.read())

Still Dre Day
>>> with open('allure.txt', 'r') as f:
        print(f.read())

The allure of breaking the law
Was always too much for me to ever ignore
```

# Installation

To install `fileguard`, simply use pip:

```
pip install fileguard
```

# Requirements

* Python `3.6+`. It should work on other Python `3.X` versions too.

This library has no external dependencies.

# Where and When Is FileGuard Useful?

This library is useful in various scenarios, specially in testing, as it
allows you to save a lot of boilerplate and error-prone code.

For example,
let's say that the program that you are developing reads an writes to
a configuration file. In your tests, you manually create a configuration file
and then want to test that your program interacts with it in the expected
manner.

In one of your test functions you want to write tests for when the
a function that updates the configuration file with invalid data and then
your program reads it in. In another test function you want to test that
the program does not crash if the configuration file is deleted. Another test
function tests the case where a deleted configuration file is updated. In yet another
test function you want to test that changing the contents of the configuration
file works as expected. You are only interested in testing how your program
reacts to changes of the configuration file in the scope of each one of those
test functions. After those, you want the contents of the original
configuration file to be restored.

If done manually you have two options:

* write boilerplate code to back up and restore the contents of the file
before and after each test function, respectively
* have a lot of copies of configuration files (one for invalid data, one with
  empty data, one with non-existent data, etc). At the end, you would still
  be left with the task of restoring the contents of the edited/deleted files

Keep in mind, that the example described above is rather simple. What if:

* you want to preserve the contents of multiple files
* you want to preserve the contents, not just of a file, but of the whole
directory
* you're not dealing with `UTF-8` encoded text files, but rather with
binaries, music files, images, etc
* you want to preserve the contents of the file in a scope inside a function
(e.g. within an `with` block) and not the of the whole function

All of those add complexity to the error-prone boilerplate code and make
it dirty, complex, hard to maintain and confusing.

The `fileguard` library allows you to tackle those problems in a clean,
Pythonic way. All you have to do is decorate the test function with `@guard`

# API Documentation and Examples

In the text that follows, **"fileguarded"** means that the contents of the
file(s) and/or directory(ies) will be preserved. In other words, their
content after the end of the scope will be the same as it was right
before the beginning of the scope.

In order to use `fileguard`, all you have to do is import `guard`:

```python
from fileguard import guard
```

`guard` can be used as a:

* function/method decorator
  * the scope of the function will be file-guarded

  ```python
  @guard('my_file.txt')
  def change_my_file():
    # Within this function, change the contents of the file as you wish.
    # You can even delete it.
    # After the function has executed, 'my_file.txt's contents will be
    #   the same as they were right before the execution of this function.

  ```

* class decorator
  * all of the **user-defined** methods will be file-guarded.
  The following two code snippets are equivalent:

  ```python
  @guard('my_file.txt')
  class MyClass(object):

    def __init__(self, my_arg_1, my_arg_2):
      self._my_arg_1 = my_arg_1
      self._my_arg_2 = my_arg_2

    def my_method_1(self):
      # code here

    def my_method_2(self):
      # code here

  ```

  ```python
  class MyClass(object):

    def __init__(self, my_arg_1, my_arg_2):
      self._my_arg_1 = my_arg_1
      self._my_arg_2 = my_arg_2

    @guard('my_file.txt')
    def my_method_1(self):
      # code here

    @guard('my_file.txt')
    def my_method_2(self):
      # code here
  ```

* context manager
  * all of the code within the `with` block is file-guarded, including
  calls to functions that change the contents of the fileguarded
  files and directories.

  ```python
  with guard('my_file.txt'):
    # Within "with" block, change the contents of the file as you wish.
    # You can even delete it.
    # After the "with" scope has ended, 'my_file.txt's contents will be
    #   the same as they were right before the execution of this with block.
  ```


## What If The File/Directory Is Deleted?

* The files will be restored, even if you **delete** them.

* The complete contents of the directory will be restored, even if you
**delete** the whole directory or some files from within it.

## Arguments

`guard()` accepts the list of files and directories to fileguard. It can take
a single argument:

```python
@guard('file.txt')
def my_function(arg1, arg2):
  # code here
```

or multiple ones:

```python
@guard('file_1.txt', 'file_2.txt')
def my_function(arg1, arg2):
  # code here
```

the snippet above is equivalent to:

```python
@guard('file_2.txt')
@guard('file_1.txt')
def my_function(arg1, arg2):
  # code here
```

In that case, the contents of all of the files passed as argument will be
fileguarded.

You can pass a file, a directory or a mixture of them as an arguments:

```python
@guard('file_1.txt', 'directory_1', '/home/iluxonchik/directory_2', '/home/iluxonchik/file_2.txt')
def my_function(arg1, arg2):
  # code here
```

In that case, the contents of the file `./file_1.txt`, directory `./directory_1`,
directory `/home/iluxonchik/directory_2` and file `/home/iluxonchik/file_2.txt`
will be fileguarded.

The fileguarded files and directories **do not need to exist at the moment of decoration**.
You can fileguard a file or directory in function, method and or a class (by decorating it with `guard()`),
without that file or directory existing yet. You have to make sure that the file
exists **when the decorated function or method is executed**.
If, however, you are using `guard()` as a context manager, you have to make sure that
the protected file or directory **does exist** at the moment when you use
`with guard():`

## Supported File Types

Any file type is supported. You can guard a text file, a binary, an music
file, an image file, a video file, etc. Under the hood, the original file
is backed up by its copy.

## Directories

Just like files, directories can contain arbitrary files. The original
directory and its contents will be restored. Under the hood, the original
directory is backed up by a copy of all of its contents.

## File-Guarded Functions Calling File-Guarded Functions (Nested Calls)

The backup order is preserved. Internally, a stack is used. The best
way to illustrate this is with an example.

Let's consider that you have a file `lets_ride.txt` with the following
content:

```
        It’s a new day, and if you ever knew Dre

```

Also, `fileguard_demo.py` contents are as follows:

```python
""" Contents of fileguard_demo.py"""

from fileguard import guard

def print_file_content():
    with open('lets_ride.txt', 'r') as f:
        print(f.read())

def append_text_to_file(text):
    with open('lets_ride.txt', 'a') as f:
            f.write(text)

@guard('lets_ride.txt')
def change_file_1():
    print('Content before change_file_1:')
    print_file_content()

    append_text_to_file('\tSame Chronic, just a different smoke\n')

    print('Content after change_file_1:')
    print_file_content()

@guard('lets_ride.txt')
def change_file_2():
    print('Content before change_file_2:')
    print_file_content()

    append_text_to_file('\tSame Impala, different spokes\n')

    change_file_1()

    print('Content after change_file_2:')
    print_file_content()

@guard('lets_ride.txt')
def change_file_3():
    print('Content before change_file_3:')
    print_file_content()

    append_text_to_file('\tYou would say I was The New Dre\n')

    change_file_2()

    print('Content after change_file_3:')
    print_file_content()

print('Intial file content:')
print_file_content()

with guard('lets_ride.txt'):
    print('Content before with:')
    print_file_content()

    change_file_3()

    print('Content after with:')
    print_file_content()

print('Final file content:')
print_file_content()
```

The output of running `python fileguard_demo.py` is the following:

```
Intial file content:
        It’s a new day, and if you ever knew Dre

Content before with:
        It’s a new day, and if you ever knew Dre

Content before change_file_3:
        It’s a new day, and if you ever knew Dre

Content before change_file_2:
        It’s a new day, and if you ever knew Dre
        You would say I was The New Dre

Content before change_file_1:
        It’s a new day, and if you ever knew Dre
        You would say I was The New Dre
        Same Impala, different spokes

Content after change_file_1:
        It’s a new day, and if you ever knew Dre
        You would say I was The New Dre
        Same Impala, different spokes
        Same Chronic, just a different smoke

Content after change_file_2:
        It’s a new day, and if you ever knew Dre
        You would say I was The New Dre
        Same Impala, different spokes

Content after change_file_3:
        It’s a new day, and if you ever knew Dre
        You would say I was The New Dre

Content after with:
        It’s a new day, and if you ever knew Dre

Final file content:
        It’s a new day, and if you ever knew Dre

```
