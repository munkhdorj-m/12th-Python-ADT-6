# ADT 5 — Linear and Circular Queues

Read the Abstract Data Types lecture (Queue section) before you start.
https://drive.google.com/file/d/1jXGQdSvuUYjGXl-PUuHMUzKWEBGQoARL/view?usp=sharing


**The scenario**

A small bank has room for **5 customers inside**. Everyone else waits in a
line **outside**.

    OUTSIDE (linear queue, 8 places)        INSIDE (circular queue, 5 places)
    ┌───┬───┬───┬───┬───┬───┬───┬───┐       ┌───┬───┬───┬───┬───┐
    │ F │ G │   │   │   │   │   │   │  ──►  │ A │ B │ C │ D │ E │  ──► served
    └───┴───┴───┴───┴───┴───┴───┴───┘       └───┴───┴───┴───┴───┘

---

## Exercise 1

**Problem:**

Build the **linear queue** for the line outside.

Set up the queue:

- `LinearQueue` → a global array of **8** elements, all set to `""` (empty string)
- `LinearHead` and `LinearTail` → global integers, both set to `-1`

Then write three functions:

`LinearEnqueue(Name)`

- If the queue is full (`LinearTail` is 7), return `False`
- Otherwise add 1 to `LinearTail`, store `Name` at `LinearQueue[LinearTail]`,
  and return `True`
- If this is the **first** item ever (`LinearHead` is -1), set `LinearHead` to 0

`LinearDequeue()`

- If the queue is empty (`LinearHead` is -1, or `LinearHead` is more than
  `LinearTail`), return `""`
- Otherwise return the name at `LinearQueue[LinearHead]`, and add 1 to `LinearHead`

`LinearCount()`

- Return how many names are waiting in the queue, using **only** `LinearHead`
  and `LinearTail`
- Return `0` if nothing was ever added

**Example:**

    Input:
      LinearEnqueue("Bat")
      LinearEnqueue("Saraa")
      LinearEnqueue("Anu")
      print(LinearCount())
      print(LinearDequeue())
      print(LinearCount())
      print(LinearHead, LinearTail)

    Output:
      3
      Bat
      2
      1 2

*Hint:* if `LinearHead` is 1 and `LinearTail` is 2, the items are at index 1
and index 2 — that is **2** items, not 1. Check your sum with the example.

---

## Exercise 2

**Problem:**

Build the **circular queue** for the people inside.

Set up the queue:

- `CircularQueue` → a global array of **5** elements, all set to `""`
- `CircularHead` and `CircularTail` → global integers, both set to `-1`
- `NumberItems` → a global integer, set to `0`

Then write three functions:

`CircularEnqueue(Name)`

- If the queue is full (`NumberItems` is 5), return `False`
- If the queue is empty, set `CircularHead` and `CircularTail` to 0
- Otherwise add 1 to `CircularTail` — and if it reaches **5**, set it back to **0**
- Store `Name` at `CircularQueue[CircularTail]`, add 1 to `NumberItems`, return `True`

`CircularDequeue()`

- If the queue is empty (`NumberItems` is 0), return `""`
- Otherwise read the name at `CircularQueue[CircularHead]`
- Add 1 to `CircularHead` — and if it reaches **5**, set it back to **0**
- Take 1 off `NumberItems`
- If the queue is now empty, set `CircularHead` and `CircularTail` back to `-1`
- Return the name

`GetItem(Position)`

- Return the name at `Position` places from the **front** of the queue
  (`Position` 0 is the front)
- If there is no item at that position, return `""`
- Do **not** change the queue

**Example:**

    Input:
      Enqueue A, B, C, D, E
      CircularDequeue()
      CircularDequeue()
      CircularDequeue()
      CircularEnqueue("F")
      CircularEnqueue("G")
      print(CircularHead, CircularTail)
      print(GetItem(0), GetItem(2), GetItem(3))
      print(GetItem(4))

    Output:
      3 1
      D F G
      ""

What the array looks like:

    index:           0    1    2    3    4
    CircularQueue: [ F    G    C    D    E ]
                         ↑              ↑
                    CircularTail   CircularHead

    Queue order:  D (pos 0)   E (pos 1)   F (pos 2)   G (pos 3)

*Hint:* the item at `Position` is at index `CircularHead + Position` — but
if that goes past the end of the array, it must wrap back to the start.

---

## Exercise 3

**Problem:**

Use **both** queues to run the bank.

`Arrive(Name)`

- If there is space **inside**, add the customer to the circular queue and
  return `"inside"`
- Otherwise add them to the line **outside** (the linear queue) and return `"outside"`
- If the line outside is also full, return `"full"`

`Serve()`

- Remove the customer at the **front** of the circular queue — they are served
- If the inside was empty, return `""`
- If anyone is waiting **outside**, move the person at the front of the line
  outside **into** the circular queue
- Return the name of the customer who was served

Use your functions from Exercises 1 and 2 — `Arrive` and `Serve` must call
the Enqueue and Dequeue functions of **both** queues.

**Example:**

    Input:
      for Name in ["A", "B", "C", "D", "E", "F", "G"]:
          print(Name, Arrive(Name))
      print(Serve())
      print(LinearCount())

    Output:
      A inside
      B inside
      C inside
      D inside
      E inside
      F outside
      G outside
      A
      1

After `A` is served, `F` moves inside. Customers are always served in the
order they arrived: A, B, C, D, E, F, G.

**Think about it:** the line outside is a **linear** queue. After 8 people in
total have waited outside, `Arrive()` returns `"full"` when the bank is full —
even if nobody is waiting outside any more. Why? What would fix it?

---
