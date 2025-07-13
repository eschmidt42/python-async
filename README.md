# Python async


## References

* mcoding videos
  * [x] [async intro](https://youtu.be/ftmdDlwMwwQ?si=h__zw_jOcgu_uk2v)
    * `python src/python_async/mcoding/intro.py`
  * [x] [async loops](https://youtu.be/dEZKySL3M9c?si=Te6GB75WsDLyzNEf)
    * `python src/python_async/mcoding/for_loop/server.py` and `python src/python_async/mcoding/for_loop/client.py`
  * [ ] [async web apps](https://youtu.be/oYrnTQAFH1Q?si=1CFzaqQ6OuTwuUvC)
  * [x] [slow async code](https://youtu.be/m_a0fN48Alw?si=t9DeVmpV3bp7TPXH)
  * [ ] [async functions vs classes](https://youtu.be/ai7y--6ElAE?si=c-aNmfwBRy306cBN)
  * [ ] [async loop pitfall](https://youtu.be/N56Jrqc7SBk?si=UHr43C-a79T8-X0W)

## Aspects to investigate

* [ ] async tasks
* [ ] async semaphores
* [x] async loops
* [ ] (async) Queue
* [ ] (async) iterators
* [ ] (async) generators
* [x] testing async code using [pytest-asyncio](https://pypi.org/project/pytest-asyncio/)
* common async pitfalls
* [x] [pyleak](https://github.com/deepankarm/pyleak) - detecting async things
* [x] [pip-audit](https://github.com/pypa/pip-audit) in pre-commit
* [x] sort multithreading vs multiprocessing
* [x] sort "thread-safe" -> [wiki](https://en.wikipedia.org/wiki/Thread_safety)
* [ ] go through High-level APIs [page](https://docs.python.org/3/library/asyncio.html)
* encode
  * [httpx](https://github.com/encode/httpx)
  * [starlette](https://github.com/encode/starlette)
  * [uvicorn](https://github.com/encode/uvicorn)

## multithreading vs multiprocessing

In Python, multithreading and multiprocessing are two distinct approaches to achieving concurrent execution, but they differ in how they utilize system resources and handle the Global Interpreter Lock (GIL).

Here's a breakdown of the key differences:

* Execution Model
  * Multithreading: In multithreading, a single process generates multiple threads that run concurrently. These threads share the same memory space within that process. 1
  * Multiprocessing: In multiprocessing, multiple processes run simultaneously, each with its own independent memory space. These processes can run across multiple CPU cores. 2

* Concurrency vs. Parallelism
  * Multithreading: Primarily implements concurrency. Due to the GIL, Python's multithreading typically doesn't achieve true parallelism for CPU-bound tasks. The GIL ensures that only one thread can execute Python bytecode at a time, even on multi-core processors.
  * Multiprocessing: Implements parallelism. Since each process has its own Python interpreter and memory space, multiprocessing can fully utilize multiple CPU cores, making it suitable for CPU-bound tasks. 2

* Resource Sharing
  * Multithreading: Threads within the same process share memory, making data sharing between them relatively easy but also requiring careful synchronization to prevent race conditions.
  * Multiprocessing: Processes have separate memory spaces, which means data sharing between them requires inter-process communication mechanisms (e.g., pipes, queues, shared memory).

* Overhead
  * Multithreading: Generally has lower overhead in terms of memory and startup time compared to multiprocessing, as threads are lighter-weight than processes.
  * Multiprocessing: Involves higher overhead due to the creation of separate processes, each with its own interpreter and memory.

* Use Cases
  * Multithreading: Best suited for I/O-bound tasks (e.g., network requests, file operations) where the program spends most of its time waiting for external resources, as the GIL is released during I/O operations, allowing other threads to run.
  * Multiprocessing: Ideal for CPU-bound tasks (e.g., heavy computations, data processing) that can benefit from parallel execution on multiple CPU cores, as it bypasses the GIL.

In summary, while both aim for concurrent execution, multiprocessing is generally preferred in Python for achieving true parallelism and utilizing multiple CPU cores for computationally intensive tasks, whereas multithreading is more effective for managing concurrent I/O operations.

[^1]: [Multithreading VS Multiprocessing in Python | by Amine Baatout](https://medium.com/contentsquare-engineering-blog/multithreading-vs-multiprocessing-in-python-ece023ad55a#:~:text=Multithreading%20took,20%20seconds%2C&text=If%20you,previous%20one.)
[^2]: [Understanding Multithreading and Multiprocessing in Python](https://medium.com/@moraneus/understanding-multithreading-and-multiprocessing-in-python-1ed39bb078d5#:~:text=To%20understand,and%2010)

## iterables, iterators and generators

In Python, iterables, iterators, and generators are fundamental concepts for handling sequences of data efficiently. While related, they represent distinct roles in how data is accessed and processed.

### Iterables

An **iterable** is any Python object that can be looped over, or "iterated" upon. This means it's an object from which an iterator can be obtained. Common examples include lists, tuples, strings, and dictionaries.

*   **Characteristics:**
    *   They implement the ```__iter__()``` method, which returns an iterator.
    *   They can be used directly in a ```for``` loop.
*   **Example:**

    ```python
    my_list = [1, 2, 3, 4] # A list is an iterable
    for item in my_list:
        print(item)
    ```

### Iterators

An **iterator** is an object that represents a stream of data. It's responsible for keeping track of the current position in the iteration and providing the next item.

*   **Characteristics:**
    *   They implement both the ```__iter__()``` method (which returns ```self```) and the ```__next__()``` method.
    *   The ```__next__()``` method returns the next item in the sequence. If there are no more items, it raises a ```StopIteration``` exception.
    *   Once an iterator is exhausted, it cannot be reused. You need to get a new iterator from the iterable.
*   **How to get an iterator:** You can obtain an iterator from an iterable using the built-in ```iter()``` function.
*   **Example:**

    ```python
    my_list = [1, 2, 3, 4]
    my_iterator = iter(my_list) # Get an iterator from the list

    print(next(my_iterator)) # Output: 1
    print(next(my_iterator)) # Output: 2
    print(next(my_iterator)) # Output: 3
    print(next(my_iterator)) # Output: 4

    try:
        print(next(my_iterator))
    except StopIteration:
        print("Iterator exhausted!")
    ```

### Generators

A **generator** is a special type of iterator that is defined using a function with the ```yield``` keyword instead of ```return```. When a generator function is called, it returns a generator object (which is itself an iterator). The ```yield``` keyword pauses the function's execution and saves its state, allowing it to resume from where it left off the next time ```__next__()``` is called.

*   **Characteristics:**
    *   They are functions that contain one or more ```yield``` statements.
    *   They automatically implement the iterator protocol (```__iter__()``` and ```__next__()```).
    *   They are memory-efficient because they generate values on the fly, one at a time, rather than storing all values in memory. This makes them ideal for large or infinite sequences.
    *   They maintain their internal state between calls.
*   **Example:**

    ```python
    def count_up_to(max_num):
        n = 1
        while n <= max_num:
            yield n # Pauses execution and yields a value
            n += 1

    # Calling the generator function returns a generator object (an iterator)
    my_generator = count_up_to(3)

    print(next(my_generator)) # Output: 1
    print(next(my_generator)) # Output: 2
    print(next(my_generator)) # Output: 3

    try:
        print(next(my_generator))
    except StopIteration:
        print("Generator exhausted!")

    # Generators can also be used directly in for loops
    print("\nUsing generator in a for loop:")
    for num in count_up_to(5):
        print(num)
    ```

### Summary of Differences

| Feature        | Iterable                                  | Iterator                                  | Generator                                     |
| :------------- | :---------------------------------------- | :---------------------------------------- | :-------------------------------------------- |
| **Definition** | An object that can be looped over.        | An object that keeps track of iteration.  | A function that produces an iterator (using ```yield```). |
| **Methods**    | Implements ```__iter__()```.                  | Implements ```__iter__()``` and ```__next__()```. | Automatically implements ```__iter__()``` and ```__next__()```. |
| **Creation**   | Built-in types (list, tuple, str, dict) or custom classes with ```__iter__()```. | Obtained from an iterable using ```iter()```. | Defined using ```def``` and ```yield```.              |
| **Memory**     | May store all elements in memory.         | Provides elements one by one.             | Generates elements on demand, memory-efficient. |
| **Reusability**| Can be iterated multiple times (new iterator each time). | Can be iterated only once.                | Can be iterated only once (unless the function is called again). |
| **Purpose**    | Represents a collection of items.         | Provides a way to access items sequentially. | Efficiently creates iterators for large/infinite sequences. |
