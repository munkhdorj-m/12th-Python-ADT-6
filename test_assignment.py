import ast
import importlib
import inspect
import textwrap

import pytest

import assignment


@pytest.fixture
def q():
    return importlib.reload(assignment)


def calls_in(function):
    tree = ast.parse(textwrap.dedent(inspect.getsource(function)))
    names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                names.append(node.func.id)
            if isinstance(node.func, ast.Attribute):
                names.append("." + node.func.attr)
    return names


def check_no_list_methods(function):
    for name in calls_in(function):
        if name in [".append", ".pop", ".insert", ".remove", ".extend", ".clear"]:
            pytest.fail(
                function.__name__ + "() uses " + name + "(). "
                "Move the pointers yourself and store with Queue[pointer] = ..."
            )


def test1_initial_queue(q):
    assert q.LinearQueue == ["", "", "", "", "", "", "", ""]
    assert q.LinearHead == -1
    assert q.LinearTail == -1


def test1_enqueue(q):
    assert q.LinearEnqueue("Bat") == True
    assert q.LinearHead == 0
    assert q.LinearTail == 0
    assert q.LinearQueue[0] == "Bat"
    assert q.LinearEnqueue("Saraa") == True
    assert q.LinearHead == 0
    assert q.LinearTail == 1
    assert q.LinearQueue[1] == "Saraa"


def test1_enqueue_when_full(q):
    for name in ["A", "B", "C", "D", "E", "F", "G", "H"]:
        assert q.LinearEnqueue(name) == True
    assert q.LinearEnqueue("I") == False
    assert q.LinearTail == 7
    assert q.LinearQueue == ["A", "B", "C", "D", "E", "F", "G", "H"]


def test1_dequeue(q):
    q.LinearEnqueue("Bat")
    q.LinearEnqueue("Saraa")
    q.LinearEnqueue("Anu")
    assert q.LinearDequeue() == "Bat"
    assert q.LinearHead == 1
    assert q.LinearDequeue() == "Saraa"
    assert q.LinearDequeue() == "Anu"


def test1_dequeue_when_empty(q):
    assert q.LinearDequeue() == ""
    q.LinearEnqueue("Bat")
    q.LinearDequeue()
    assert q.LinearDequeue() == ""


def test1_count(q):
    assert q.LinearCount() == 0
    q.LinearEnqueue("A")
    q.LinearEnqueue("B")
    q.LinearEnqueue("C")
    assert q.LinearCount() == 3
    q.LinearDequeue()
    assert q.LinearCount() == 2
    q.LinearDequeue()
    q.LinearDequeue()
    assert q.LinearCount() == 0
    assert q.LinearDequeue() == ""
    assert q.LinearCount() == 0


def test1_uses_pointers(q):
    check_no_list_methods(q.LinearEnqueue)
    check_no_list_methods(q.LinearDequeue)
    for x in range(10):
        q.LinearEnqueue("P" + str(x))
    for x in range(10):
        q.LinearDequeue()
    assert len(q.LinearQueue) == 8
    assert q.LinearTail == 7


def test2_initial_queue(q):
    assert q.CircularQueue == ["", "", "", "", ""]
    assert q.CircularHead == -1
    assert q.CircularTail == -1
    assert q.NumberItems == 0


def test2_enqueue_and_dequeue(q):
    assert q.CircularEnqueue("Bat") == True
    assert q.CircularHead == 0
    assert q.CircularTail == 0
    assert q.NumberItems == 1
    assert q.CircularEnqueue("Saraa") == True
    assert q.CircularEnqueue("Anu") == True
    assert q.NumberItems == 3
    assert q.CircularDequeue() == "Bat"
    assert q.CircularHead == 1
    assert q.NumberItems == 2
    assert q.CircularDequeue() == "Saraa"


def test2_wraps_around(q):
    for name in ["A", "B", "C", "D", "E"]:
        assert q.CircularEnqueue(name) == True
    assert q.CircularEnqueue("X") == False
    assert q.CircularDequeue() == "A"
    assert q.CircularDequeue() == "B"
    assert q.CircularEnqueue("F") == True
    assert q.CircularTail == 0
    assert q.CircularQueue[0] == "F"
    assert q.CircularEnqueue("G") == True
    assert q.CircularTail == 1
    assert q.CircularEnqueue("H") == False
    result = []
    for x in range(5):
        result.append(q.CircularDequeue())
    assert result == ["C", "D", "E", "F", "G"]


def test2_empty_resets_pointers(q):
    assert q.CircularDequeue() == ""
    q.CircularEnqueue("Bat")
    q.CircularEnqueue("Saraa")
    q.CircularDequeue()
    q.CircularDequeue()
    assert q.NumberItems == 0
    assert q.CircularHead == -1
    assert q.CircularTail == -1
    assert q.CircularDequeue() == ""


def test2_get_item(q):
    assert q.GetItem(0) == ""
    q.CircularEnqueue("Bat")
    q.CircularEnqueue("Saraa")
    q.CircularEnqueue("Anu")
    assert q.GetItem(0) == "Bat"
    assert q.GetItem(1) == "Saraa"
    assert q.GetItem(2) == "Anu"
    assert q.GetItem(3) == ""
    assert q.GetItem(-1) == ""
    assert q.NumberItems == 3
    assert q.CircularHead == 0


def test2_get_item_after_wrap(q):
    for name in ["A", "B", "C", "D", "E"]:
        q.CircularEnqueue(name)
    q.CircularDequeue()
    q.CircularDequeue()
    q.CircularDequeue()
    q.CircularEnqueue("F")
    q.CircularEnqueue("G")
    assert q.GetItem(0) == "D"
    assert q.GetItem(1) == "E"
    assert q.GetItem(2) == "F"
    assert q.GetItem(3) == "G"
    assert q.GetItem(4) == ""
    assert q.CircularDequeue() == "D"


def test2_uses_pointers(q):
    check_no_list_methods(q.CircularEnqueue)
    check_no_list_methods(q.CircularDequeue)
    for x in range(20):
        q.CircularEnqueue("P" + str(x))
        q.CircularDequeue()
    assert len(q.CircularQueue) == 5
    assert q.NumberItems == 0


def test3_arrive(q):
    for name in ["A", "B", "C", "D", "E"]:
        assert q.Arrive(name) == "inside"
    assert q.Arrive("F") == "outside"
    assert q.Arrive("G") == "outside"
    assert q.NumberItems == 5
    assert q.LinearCount() == 2


def test3_serve_order(q):
    for name in ["A", "B", "C", "D", "E", "F", "G"]:
        q.Arrive(name)
    assert q.Serve() == "A"
    assert q.NumberItems == 5
    assert q.LinearCount() == 1
    assert q.CircularQueue[q.CircularTail] == "F"
    assert q.Serve() == "B"
    assert q.LinearCount() == 0
    served = []
    for x in range(5):
        served.append(q.Serve())
    assert served == ["C", "D", "E", "F", "G"]
    assert q.NumberItems == 0


def test3_serve_when_empty(q):
    assert q.Serve() == ""
    q.Arrive("A")
    assert q.Serve() == "A"
    assert q.Serve() == ""


def test3_outside_line_is_linear(q):
    for x in range(13):
        assert q.Arrive("P" + str(x)) in ["inside", "outside"]
    assert q.Arrive("P13") == "full"
    for x in range(8):
        q.Serve()
    assert q.NumberItems == 5
    assert q.LinearCount() == 0
    for x in range(5):
        q.Serve()
    assert q.Arrive("Late1") == "inside"
    for x in range(4):
        q.Arrive("Late" + str(x + 2))
    assert q.Arrive("Late6") == "full"


def test3_uses_both_queues(q):
    arrive_calls = calls_in(q.Arrive)
    serve_calls = calls_in(q.Serve)
    assert "CircularEnqueue" in arrive_calls, "Arrive() must call CircularEnqueue()."
    assert "LinearEnqueue" in arrive_calls, "Arrive() must call LinearEnqueue()."
    assert "CircularDequeue" in serve_calls, "Serve() must call CircularDequeue()."
    assert "LinearDequeue" in serve_calls, "Serve() must call LinearDequeue()."
    q.Arrive("A")
    assert q.Serve() == "A"
